import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# --------------------------------------------------
# FILE LOCATIONS
# --------------------------------------------------

DATASET_PATH = "dataset/emergency_data.csv"
MODEL_PATH = "model/emergency_model.pkl"


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

print("=" * 50)
print("RAKSHAYAN AI - MODEL TRAINING")
print("=" * 50)

print("\nLoading dataset...")

data = pd.read_csv(DATASET_PATH)

print(f"Total training examples: {len(data)}")

print("\nIntent categories:")

print(data["intent"].value_counts())


# --------------------------------------------------
# PREPARE DATA
# --------------------------------------------------

X = data["text"]
y = data["intent"]


# --------------------------------------------------
# SPLIT DATA
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# --------------------------------------------------
# CREATE AI MODEL
# --------------------------------------------------

model = Pipeline([

    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )
    ),

    (
        "classifier",
        LogisticRegression(
            max_iter=2000
        )
    )

])


# --------------------------------------------------
# TRAIN
# --------------------------------------------------

print("\nTraining Rakshayan AI...")

model.fit(X_train, y_train)


# --------------------------------------------------
# TEST
# --------------------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)


print("\nTraining completed!")

print(
    f"Model accuracy: {accuracy * 100:.2f}%"
)


# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

print("\nSaving trained model...")

model_path = MODEL_PATH

joblib.dump(
    model,
    model_path
)


print("\nModel successfully saved!")

print(
    f"Location: {model_path}"
)

print("\nRakshayan AI brain is ready! 🧠")

print("=" * 50)