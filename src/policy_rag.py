
# src/policy_rag.py

from pathlib import Path
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# 1. PROJECT PATH
# --------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

POLICY_DIR = ROOT_DIR / "data" / "policies"
EVAL_PATH = ROOT_DIR / "data" / "processed" / "policy_eval_clean.csv"
OUTPUT_DIR = ROOT_DIR / "outputs"
OUTPUT_PATH = OUTPUT_DIR / "policy_evaluation.csv"


# --------------------------------------------------
# 2. LOAD POLICY DOCUMENTS
# --------------------------------------------------

policy_docs = []

for file_path in sorted(POLICY_DIR.glob("*.txt")):
    text = file_path.read_text(encoding="utf-8")

    policy_docs.append({
        "name": file_path.name,
        "text": text
    })

if not policy_docs:
    raise FileNotFoundError(
        f"No policy files found in {POLICY_DIR}"
    )

print("Loaded policy documents:", len(policy_docs))

for doc in policy_docs:
    print("-", doc["name"])


# --------------------------------------------------
# 3. LOAD EVALUATION DATA
# --------------------------------------------------

policy = pd.read_csv(EVAL_PATH)

print("\nPolicy dataset shape:", policy.shape)
print("Policy columns:", policy.columns.tolist())


# --------------------------------------------------
# 4. BUILD TF-IDF INDEX
# --------------------------------------------------

documents = [doc["text"] for doc in policy_docs]

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2),
    sublinear_tf=True
)

doc_vectors = vectorizer.fit_transform(documents)


# --------------------------------------------------
# 5. POLICY RETRIEVAL FUNCTION
# --------------------------------------------------

def retrieve_policy(question, top_k=2):

    query_vector = vectorizer.transform([question])

    scores = cosine_similarity(
        query_vector,
        doc_vectors
    )[0]

    top_indices = scores.argsort()[::-1][:top_k]

    results = []

    for index in top_indices:

        if scores[index] > 0:

            results.append({
                "name": policy_docs[index]["name"],
                "text": policy_docs[index]["text"],
                "score": float(scores[index])
            })

    return results


# --------------------------------------------------
# 6. EVALUATE POLICY RETRIEVAL
# --------------------------------------------------

evaluation_results = []

correct = 0

for _, row in policy.iterrows():

    question = str(row["question"])
    expected_doc = str(row["expected_doc"])

    retrieved = retrieve_policy(question, top_k=2)

    retrieved_docs = [
        item["name"] for item in retrieved
    ]

    # Questions with expected_doc = NONE
    if expected_doc.upper() == "NONE":

        hit = len(retrieved_docs) == 0

    else:

        hit = expected_doc in retrieved_docs

    if hit:
        correct += 1

    evaluation_results.append({
        "question": question,
        "expected_doc": expected_doc,
        "retrieved_docs": ", ".join(retrieved_docs),
        "retrieval_hit": int(hit),
        "top_score": (
            retrieved[0]["score"] if retrieved else 0.0
        )
    })


# --------------------------------------------------
# 7. SAVE RESULTS
# --------------------------------------------------

results_df = pd.DataFrame(evaluation_results)

total_questions = len(results_df)

accuracy = (
    correct / total_questions * 100
    if total_questions > 0
    else 0
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

results_df.to_csv(OUTPUT_PATH, index=False)


# --------------------------------------------------
# 8. DISPLAY SUMMARY
# --------------------------------------------------

print("\n" + "=" * 40)
print("POLICY EVALUATION")
print("=" * 40)

print("Total questions:", total_questions)
print("Correct retrieval:", correct)
print(f"Retrieval accuracy: {accuracy:.2f}%")

print("\nEvaluation details:")
print(
    results_df[
        ["question", "expected_doc", "retrieved_docs", "retrieval_hit"]
    ].to_string(index=False)
)

print("\nSaved:", OUTPUT_PATH)
