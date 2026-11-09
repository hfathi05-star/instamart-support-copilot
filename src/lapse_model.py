
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)

# Load lapse dataset
df = pd.read_csv("data/processed/lapse_dataset.csv")

# Features and target
features = ["age"]
X = df[features]
y = df["lapsed"]
#Handle Missing Values
X = X.fillna(0)
# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Logistic Regression
logistic_model = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(class_weight="balanced", random_state=42))
])

logistic_model.fit(X_train, y_train)
logistic_pred = logistic_model.predict(X_test)
logistic_prob = logistic_model.predict_proba(X_test)[:, 1]

# Random Forest
rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)
rf_prob = rf_model.predict_proba(X_test)[:, 1]

# Evaluation function
def evaluate_model(name, y_true, pred, prob):
    print("\n", name)
    print("Accuracy:", round(accuracy_score(y_true, pred), 3))
    print("Precision:", round(precision_score(y_true, pred, zero_division=0), 3))
    print("Recall:", round(recall_score(y_true, pred, zero_division=0), 3))
    print("F1 Score:", round(f1_score(y_true, pred, zero_division=0), 3))
    print("ROC-AUC:", round(roc_auc_score(y_true, prob), 3))
    print(classification_report(y_true, pred, zero_division=0))

# Evaluate
evaluate_model("LOGISTIC REGRESSION", y_test, logistic_pred, logistic_prob)
evaluate_model("RANDOM FOREST", y_test, rf_pred, rf_prob)

print("\nLAPSE MODEL TRAINING COMPLETED!")
