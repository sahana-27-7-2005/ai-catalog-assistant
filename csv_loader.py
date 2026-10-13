import pandas as pd

def load_csv_as_text(csv_path):
    df = pd.read_csv(csv_path)

    chunks = []
    for _, row in df.iterrows():
        text = ""
        for col, val in row.items():
            text += f"{col}: {val}\n"
        chunks.append(text.strip())

    return chunks
