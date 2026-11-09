
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/customer_segments.csv")

plt.figure(figsize=(8, 5))

plt.scatter(
    df["recency"],
    df["frequency"],
    c=df["segment"],
    cmap="viridis",
    alpha=0.7
)

plt.xlabel("Recency (Days)")
plt.ylabel("Frequency")
plt.title("Customer Segmentation Visualization")
plt.colorbar(label="Segment")

plt.savefig(
    "data/processed/customer_segments_plot.png",
    dpi=300
)

plt.show()

print("Customer segment visualization saved!")
