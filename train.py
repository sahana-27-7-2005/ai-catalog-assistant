# training.py
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from datasets import load_dataset
import torch

# -------------------------------
# 1️⃣ FORCE GPU
# -------------------------------
assert torch.cuda.is_available(), "❌ GPU not detected. Fix CUDA first."
device = torch.device("cuda")
print("✅ Using GPU")

# -------------------------------
# 2️⃣ Load dataset (ONLY 10K)
# -------------------------------
dataset = load_dataset(
    "json",
    data_files="general_qa_100000_multi_domain.json"
)["train"]

dataset = dataset.shuffle(seed=42).select(range(10000))
print(f"Dataset loaded with {len(dataset)} entries (FAST MODE)")

# -------------------------------
# 3️⃣ Preprocess
# -------------------------------
def preprocess(example):
    return {
        "input_text": f"Context: {example['context']}\nQuestion: {example['question']}\nAnswer:",
        "target_text": example["answer"]
    }

dataset = dataset.map(preprocess, remove_columns=dataset.column_names)

# -------------------------------
# 4️⃣ Load tokenizer & model
# -------------------------------
model_name = "distilgpt2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_name)
model.resize_token_embeddings(len(tokenizer))
model.config.pad_token_id = tokenizer.eos_token_id
model.to(device)

# -------------------------------
# 5️⃣ Tokenization (FAST)
# -------------------------------
MAX_LENGTH = 128

def tokenize(batch):
    inputs = tokenizer(
        batch["input_text"],
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH
    )

    targets = tokenizer(
        batch["target_text"],
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH
    )

    inputs["labels"] = targets["input_ids"]
    return inputs

dataset = dataset.map(tokenize, batched=True)
dataset.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "labels"]
)

# -------------------------------
# 6️⃣ Training arguments (GPU OPTIMIZED)
# -------------------------------
training_args = TrainingArguments(
    output_dir="./trained_assistant",
    num_train_epochs=3,
    per_device_train_batch_size=1,   # SAFE for 4GB GPU
    gradient_accumulation_steps=8,   # effective batch size = 8
    learning_rate=5e-5,
    fp16=True,
    logging_steps=200,
    save_steps=2000,
    save_total_limit=2,
    dataloader_num_workers=0,
    report_to="none"
)

# -------------------------------
# 7️⃣ Trainer
# -------------------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset
)

# -------------------------------
# 8️⃣ Train
# -------------------------------
print("🚀 Training started (GPU FAST MODE)")
trainer.train()

# -------------------------------
# 9️⃣ Save
# -------------------------------
model.save_pretrained("./trained_assistant")
tokenizer.save_pretrained("./trained_assistant")
print("✅ Training complete")
