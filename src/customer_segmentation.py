import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

df = pd.read_csv("data/processed/rfm.csv")

# Convert monetary values to numeric
df["monetary"] = pd.to_numeric(
    df["monetary"], errors="coerce"
)

# Remove invalid values
df = df.dropna(subset=["recency", "frequency"])
df["monetary"] = df["monetary"].fillna(0)
print("Customers after cleaning:",len(df))

rfm = df[["recency", "frequency", "monetary"]]

scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm)

print("K-MEANS CUSTOMER SEGMENTATION")
print("============================")

for k in range(2, 9):
    model = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = model.fit_predict(rfm_scaled)

    inertia = model.inertia_
    silhouette = silhouette_score(rfm_scaled, labels)

    print(
        f"K={k}, Inertia={inertia:.2f}, "
        f"Silhouette={silhouette:.3f}"
    )
    # Final customer segmentation
final_model = KMeans(n_clusters=2, n_init=10, random_state=42)
df["segment"] = final_model.fit_predict(rfm_scaled)

df.to_csv("data/processed/customer_segments.csv", index=False)

print("\nCUSTOMER SEGMENTS SAVED!")
print(df["segment"].value_counts())
print("\nSaved to data/processed/customer_segments.csv")