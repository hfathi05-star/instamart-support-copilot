import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

df = pd.read_csv("data/processed/lapse_dataset.csv")

X = df[["age"]].fillna(0)
y = df["lapsed"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

models = {
    "Logistic Regression Balanced": LogisticRegression(
        class_weight="balanced", random_state=42
    ),
    "Random Forest Balanced": RandomForestClassifier(
        class_weight="balanced", random_state=42
    )
}

for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    print("\n", name)
    print("Accuracy:", round(accuracy_score(y_test, pred), 3))
    print(classification_report(y_test, pred, zero_division=0))