
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
from policy_rag import retrieve_policy

# Load evaluation questions
eval_path = ROOT_DIR / "data" / "processed" / "policy_eval_clean.csv"
df = pd.read_csv(eval_path)

results = []

for _, row in df.iterrows():
    question = row["question"]
    expected_doc = row["expected_doc"]

    retrieved = retrieve_policy(question, top_k=2)

    retrieved_docs = [item["policy"] for item in retrieved]

    hit = expected_doc in retrieved_docs

    results.append({
        "question": question,
        "expected_doc": expected_doc,
        "retrieved_docs": ", ".join(retrieved_docs),
        "retrieval_hit": hit
    })

result_df = pd.DataFrame(results)

accuracy = result_df["retrieval_hit"].mean() * 100

output_path = ROOT_DIR / "outputs" / "policy_evaluation.csv"
output_path.parent.mkdir(exist_ok=True)
result_df.to_csv(output_path, index=False)

print("\nPOLICY EVALUATION")
print("Total questions:", len(result_df))
print("Correct retrieval:", result_df["retrieval_hit"].sum())
print(f"Retrieval accuracy: {accuracy:.2f}%")
print("Saved:", output_path)
