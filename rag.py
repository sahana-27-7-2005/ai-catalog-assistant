import pandas as pd

def csv_to_chunks(file_path):
    df = pd.read_csv(file_path)
    return df


def search_context(df, query, top_k=5):
    query = query.lower()

    # ✅ Get all unique categories from CSV
    categories = df["category"].str.lower().unique()

    # ✅ Auto detect category from query
    selected_category = None
    for cat in categories:
        if cat in query:
            selected_category = cat
            break

    # ✅ Filter if category found
    if selected_category:
        df = df[df["category"].str.lower() == selected_category]

    # fallback
    if df.empty:
        return "No relevant items found"

    # convert rows to text
    results = []
    for _, row in df.head(top_k).iterrows():
        text = f"{row['brand']} {row['name']} ₹{row['price']} - {row['description']}"
        results.append(text)

    return "\n".join(results)