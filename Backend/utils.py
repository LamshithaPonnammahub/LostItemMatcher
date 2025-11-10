# import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.naive_bayes import MultinomialNB
# import os
# import csv
# from sklearn.metrics.pairwise import cosine_similarity

# # Paths
# metadata_path = "dataset/metadata.csv"
# notifications_path = "dataset/notifications.csv"
# confirmations_path = "dataset/confirmations.csv"

# # Load metadata
# df = pd.read_csv(metadata_path)

# # Combine type, color, description
# df['combined'] = df['type'].str.lower() + ' ' + df['color'].str.lower() + ' ' + df['description'].str.lower()

# # Features and labels
# X = df['combined']
# y = df['filename']

# # Vectorize
# vectorizer = CountVectorizer()
# X_vectorized = vectorizer.fit_transform(X)

# # Train Naive Bayes
# clf = MultinomialNB()
# clf.fit(X_vectorized, y)


# def find_item(user_input, top_n=3):
#     """
#     user_input: dict with keys 'type', 'color', 'description'
#     Returns top_n most similar items
#     """
#     input_text = f"{user_input.get('type','')} {user_input.get('color','')} {user_input.get('description','')}".lower()
#     input_vectorized = vectorizer.transform([input_text])

#     # Predict probabilities for all items
#     predicted_proba = clf.predict_proba(input_vectorized)[0]
#     filenames = clf.classes_

#     # Combine filenames and probabilities
#     items_with_proba = list(zip(filenames, predicted_proba))

#     # Sort by probability descending
#     items_with_proba.sort(key=lambda x: x[1], reverse=True)

#     matched_items = []
#     for filename, proba in items_with_proba[:top_n]:
#         row = df[df['filename'] == filename].iloc[0]
#         matched_items.append({
#             "filename": row['filename'],
#             "description": row['description'],
#             "image_path": f"dataset/images/{row['filename']}"
#         })

#     return matched_items


# def save_notification(email, description, status="pending"):
#     """
#     Save notifications to CSV for future reference.
#     status: pending, claimed, ignored
#     """
#     file_exists = os.path.isfile(notifications_path)
#     with open(notifications_path, "a", newline="") as csvfile:
#         writer = csv.writer(csvfile)
#         if not file_exists:
#             writer.writerow(["email", "description", "status"])
#         writer.writerow([email, description, status])


# def save_confirmation(email, filename, description, status):
#     """
#     Save user confirmation (claimed/ignored) in confirmations.csv
#     """
#     file_exists = os.path.isfile(confirmations_path)
#     with open(confirmations_path, "a", newline="") as csvfile:
#         writer = csv.writer(csvfile)
#         if not file_exists:
#             writer.writerow(["email", "filename", "description", "status"])
#
#         writer.writerow([email, filename, description, status])
# #utils.py
# import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.naive_bayes import MultinomialNB
# import os
# import csv

# # Paths
# metadata_path = "dataset/metadata.csv"
# notifications_path = "dataset/notifications.csv"
# confirmations_path = "dataset/confirmations.csv"

# # Load metadata
# df = pd.read_csv(metadata_path)
# df['combined'] = df['type'] + ' ' + df['color'] + ' ' + df['description']

# # Train Naive Bayes
# vectorizer = CountVectorizer()
# X_vectorized = vectorizer.fit_transform(df['combined'])
# y = df['filename']
# clf = MultinomialNB()
# clf.fit(X_vectorized, y)

# def find_item(user_input):
#     input_text = f"{user_input.get('type','')} {user_input.get('color','')} {user_input.get('description','')}"
#     input_vectorized = vectorizer.transform([input_text])

#     probs = clf.predict_proba(input_vectorized)[0]
#     filenames = clf.classes_

#     # Sort by probability
#     sorted_items = sorted(zip(filenames, probs), key=lambda x: x[1], reverse=True)

#     results = []
#     for filename, prob in sorted_items[:3]:  # top 3 matches
#         row = df[df['filename'] == filename].iloc[0]
#         results.append({
#             "filename": row['filename'],
#             "description": row['description'],
#             "type": row['type'],
#             "color": row['color'],
#             "image_path": f"dataset/images/{row['filename']}",
#             "probability": float(prob)
#         })
#     return results

# def save_notification(email, description, status="pending"):
#     file_exists = os.path.isfile(notifications_path)
#     with open(notifications_path, "a", newline="") as csvfile:
#         writer = csv.writer(csvfile)
#         if not file_exists:
#             writer.writerow(["email", "description", "status"])
#         writer.writerow([email, description, status])

# def save_confirmation(email, filename, description, status):
#     file_exists = os.path.isfile(confirmations_path)
#     with open(confirmations_path, "a", newline="") as csvfile:
#         writer = csv.writer(csvfile)
#         if not file_exists:
#             writer.writerow(["email", "filename", "description", "status"])
#         writer.writerow([email, filename, description, status])





import pandas as pd
import os
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# File paths
metadata_path = "dataset/metadata.csv"
notifications_path = "dataset/notifications.csv"
confirmations_path = "dataset/confirmations.csv"

def load_data():
    df = pd.read_csv(metadata_path)
    df["combined"] = (df["type"] + " " + df["color"] + " " + df["description"]).str.lower()
    return df

def find_item(user_input):
    """Find items by text similarity (TF-IDF cosine)."""
    df = load_data()
    user_text = f"{user_input.get('type','')} {user_input.get('color','')} {user_input.get('description','')}".lower().strip()

    if not user_text:
        return []

    corpus = df["combined"].tolist() + [user_text]
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(corpus)

    # Compare user input (last vector) to all items
    similarities = cosine_similarity(vectors[-1], vectors[:-1]).flatten()

    # Add similarity scores
    df["similarity"] = similarities

    # Keep only strong matches (>= 0.5)
    matched = df[df["similarity"] >= 0.5].sort_values(by="similarity", ascending=False)

    results = []
    for _, row in matched.iterrows():
        results.append({
            "filename": row["filename"],
            "description": row["description"],
            "type": row["type"],
            "color": row["color"],
            "image_path": f"/images/{row['filename']}",
            "probability": round(float(row["similarity"]), 2)
        })

    print("User input:", user_text)
    print("Matched results:", results)
    return results

def save_notification(email, description, status="pending"):
    if not email:
        return
    file_exists = os.path.isfile(notifications_path)
    with open(notifications_path, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["email", "description", "status"])
        writer.writerow([email, description, status])

def save_confirmation(email, filename, description, status):
    if not filename or not description:
        return
    file_exists = os.path.isfile(confirmations_path)
    with open(confirmations_path, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["email", "filename", "description", "status"])
        writer.writerow([email, filename, description, status])


def compute_accuracy_curve(train_fracs=None, trials=3, top_k=1):
    """
    Compute accuracy across different training set fractions.
    - train_fracs: iterable of fractions (0< f <=1) to use as train size
    - trials: number of random trials per fraction (averaged)
    - top_k: whether to use top-k accuracy (1 means top-1)

    Returns dict:
      {
        'accuracy': [percentages],
        'labels': ['F10','F20',...],
        'train_counts': [n_train...],
        'test_counts': [n_test...]
      }
    Falls back to empty results if sklearn isn't available.
    """
    if train_fracs is None:
        train_fracs = [0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0]

    # Try to import sklearn here; if unavailable, raise a clear error
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
    except Exception as e:
        raise ImportError("sklearn required to compute accuracy curve: " + str(e))

    df = load_data()
    results = []
    train_counts = []
    test_counts = []

    for frac in train_fracs:
        accs = []
        n_train = 0
        n_test = 0
        for _ in range(trials):
            # sample train fraction
            if frac >= 1.0:
                train_df = df.copy()
                test_df = df.sample(frac=0.3) if len(df) > 5 else df.copy()
            else:
                train_df = df.sample(frac=frac, replace=False)
                test_df = df.drop(train_df.index)

            # If no test rows, skip this trial
            if test_df.empty or train_df.empty:
                continue

            n_train = len(train_df)
            n_test = len(test_df)

            vectorizer = TfidfVectorizer()
            train_corpus = train_df['combined'].tolist()
            train_vecs = vectorizer.fit_transform(train_corpus)

            # For each test row compute similarity to all train rows
            correct = 0
            total = 0
            for _, row in test_df.iterrows():
                query = row['combined']
                qvec = vectorizer.transform([query])
                sims = cosine_similarity(qvec, train_vecs).flatten()
                # get top_k indices from train
                top_indices = sims.argsort()[::-1][:top_k]
                top_filenames = [train_df.iloc[i]['filename'] for i in top_indices]
                # check if true filename present
                if row['filename'] in top_filenames:
                    correct += 1
                total += 1

            if total > 0:
                accs.append(correct / total)

        # average over trials
        avg_acc = float(sum(accs) / len(accs)) if accs else 0.0
        results.append(round(avg_acc * 100, 2))
        train_counts.append(n_train)
        test_counts.append(n_test)

    labels = [f"F{int(frac*100)}" for frac in train_fracs]
    return {
        "accuracy": results,
        "labels": labels,
        "train_counts": train_counts,
        "test_counts": test_counts,
        "note": "Accuracy = top-{} averaged over {} trials per fraction".format(top_k, trials),
    }
