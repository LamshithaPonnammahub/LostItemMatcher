import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import os
import csv
from sklearn.metrics.pairwise import cosine_similarity

# Paths
metadata_path = "dataset/metadata.csv"
notifications_path = "dataset/notifications.csv"
confirmations_path = "dataset/confirmations.csv"

# Load metadata
df = pd.read_csv(metadata_path)

# Combine type, color, description
df['combined'] = df['type'].str.lower() + ' ' + df['color'].str.lower() + ' ' + df['description'].str.lower()

# Features and labels
X = df['combined']
y = df['filename']

# Vectorize
vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Train Naive Bayes
clf = MultinomialNB()
clf.fit(X_vectorized, y)


def find_item(user_input, top_n=3):
    """
    user_input: dict with keys 'type', 'color', 'description'
    Returns top_n most similar items
    """
    input_text = f"{user_input.get('type','')} {user_input.get('color','')} {user_input.get('description','')}".lower()
    input_vectorized = vectorizer.transform([input_text])

    # Predict probabilities for all items
    predicted_proba = clf.predict_proba(input_vectorized)[0]
    filenames = clf.classes_

    # Combine filenames and probabilities
    items_with_proba = list(zip(filenames, predicted_proba))

    # Sort by probability descending
    items_with_proba.sort(key=lambda x: x[1], reverse=True)

    matched_items = []
    for filename, proba in items_with_proba[:top_n]:
        row = df[df['filename'] == filename].iloc[0]
        matched_items.append({
            "filename": row['filename'],
            "description": row['description'],
            "image_path": f"dataset/images/{row['filename']}"
        })

    return matched_items


def save_notification(email, description, status="pending"):
    """
    Save notifications to CSV for future reference.
    status: pending, claimed, ignored
    """
    file_exists = os.path.isfile(notifications_path)
    with open(notifications_path, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["email", "description", "status"])
        writer.writerow([email, description, status])


def save_confirmation(email, filename, description, status):
    """
    Save user confirmation (claimed/ignored) in confirmations.csv
    """
    file_exists = os.path.isfile(confirmations_path)
    with open(confirmations_path, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["email", "filename", "description", "status"])
        writer.writerow([email, filename, description, status])
