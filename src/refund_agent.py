
import sys
from pathlib import Path
import pandas as pd
policy = pd.read_csv("data/processed/policy_eval_clean.csv")

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import mockllm
from policy_rag import retrieve_policy




def refund_agent(question):
    retrieved = retrieve_policy(question, top_k=2)

    retrieved_docs = [
        item["name"] for item in (retrieved or [])
    ]

    policy_context = "\n".join(
        item["text"] for item in (retrieved or [])
    )

    messages = [
    {
        "role": "system",
        "content": "AGENT"
    },
    {
        "role": "user",
        "content": f"Question: {question}\nPolicy Context:\n{policy_context}"
    }
]

    response = mockllm.chat(messages)
    answer = response.choices[0].message.content

    return {
        "question": question,
        "retrieved_policies": retrieved_docs,
        "answer": answer
    }


if __name__ == "__main__":
    results = []

    for _, row in policy . iterrows():
        result = refund_agent(row["question"])

        results.append({
            "question": row["question"],
            "expected_doc": row["expected_doc"],
            "retrieved_policies": result["retrieved_policies"],
            "answer": result["answer"]
        })

    output = pd.DataFrame(results)
    output.to_csv("outputs/refund_agent_results.csv", index=False)

    print("\nREFUND AGENT EVALUATION")
    print("Total questions:", len(output))
    print("Saved: outputs/refund_agent_results.csv")
