
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# Load datasets
df = pd.read_csv("data/processed/lapse_dataset.csv")
rfm = pd.read_csv("data/processed/rfm.csv")

# Merge customer features
df = df.merge(rfm, on="customer_id", how="left")

# Features
features = ["age", "recency_x", "frequency", "monetary"]
print("lapse dataset columns:")
print(df.columns.tolist())
X = df[features].apply(pd. to_numeric, errors="coerce").fillna(0)
y = df["lapsed"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Random Forest tuning
rf = RandomForestClassifier(random_state=42)

params = {
    "n_estimators": [100, 200],
    "max_depth": [5, 10, None],
    "class_weight": ["balanced", "balanced_subsample"]
}

grid = GridSearchCV(
    rf, params, cv=3, scoring="f1", n_jobs=-1
)

grid.fit(X_train, y_train)

best_model = grid.best_estimator_
pred = best_model.predict(X_test)
prob = best_model.predict_proba(X_test)[:, 1]

print("BEST PARAMETERS:")
print(grid.best_params_)

print("\nBEST CV F1:", round(grid.best_score_, 3))
print("\nTEST ROC-AUC:", round(roc_auc_score(y_test, prob), 3))
print("\nCLASSIFICATION REPORT:")
print(classification_report(y_test, pred, zero_division=0))
