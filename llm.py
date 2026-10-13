import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

device = "cuda" if torch.cuda.is_available() else "cpu"

model_path = "./trained_assistant"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path).to(device)

def generate_answer(context, question):
    prompt = f"""
You are a catalog assistant.
Use ONLY the data in the context.

Context:
{context}

Question:
{question}

"""
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    output = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.3,
        top_p=0.9,
        repetition_penalty=1.1
    )

    # Decode output
    decoded = tokenizer.decode(output[0], skip_special_tokens=True)

    # ✅ Strip the prompt from the output
    answer = decoded.split("Answer:")[-1].strip()
    return answer
