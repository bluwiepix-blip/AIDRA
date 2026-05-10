"""
Machine Learning Models for AIDRA System
Includes: kNN, Naive Bayes, and evaluation metrics
Dataset loaded from: disaster_dataset.csv
"""

import csv
import os
import random


# ==========================================
# DATASET LOADER
# ==========================================
def load_dataset(filepath="disaster_dataset.csv"):
    """
    Load disaster response dataset from CSV file.
    
    Expected CSV columns:
        severity_level      : 2=critical, 1=moderate, 0=minor
        distance_to_hospital: distance in km (numeric)
        risk_zone_count     : number of risk zones on path (numeric)
        survival            : 0=Low survival chance, 1=High survival chance (label)
    
    Returns:
        X (list of feature lists), y (list of labels)
    """
    X, y = [], []

    # Support both absolute and relative paths
    if not os.path.isabs(filepath):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_dir, filepath)

    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Dataset file not found: {filepath}\n"
            f"Make sure 'disaster_dataset.csv' is in the same folder as this script."
        )

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        required_cols = {"severity_level", "distance_to_hospital", "risk_zone_count", "survival"}
        if not required_cols.issubset(set(reader.fieldnames or [])):
            missing = required_cols - set(reader.fieldnames or [])
            raise ValueError(f"CSV is missing required columns: {missing}")

        for row in reader:
            try:
                features = [
                    int(row["severity_level"]),
                    float(row["distance_to_hospital"]),
                    int(row["risk_zone_count"]),
                ]
                label = int(row["survival"])
                X.append(features)
                y.append(label)
            except ValueError as e:
                print(f"  ⚠️  Skipping invalid row {row}: {e}")

    print(f"✅ Dataset loaded: {len(X)} samples from '{os.path.basename(filepath)}'")
    print(f"   Class distribution → survival=1: {sum(y)}, survival=0: {len(y)-sum(y)}")
    return X, y


def split_dataset(X, y, test_ratio=0.2, seed=42):
    """
    Split dataset into train and test sets (no external libraries needed).
    
    Args:
        X         : feature list
        y         : label list
        test_ratio: fraction of data to use for testing (default 20%)
        seed      : random seed for reproducibility
    
    Returns:
        X_train, X_test, y_train, y_test
    """
    random.seed(seed)
    indices = list(range(len(X)))
    random.shuffle(indices)

    split_point = int(len(indices) * (1 - test_ratio))
    train_idx = indices[:split_point]
    test_idx  = indices[split_point:]

    X_train = [X[i] for i in train_idx]
    y_train = [y[i] for i in train_idx]
    X_test  = [X[i] for i in test_idx]
    y_test  = [y[i] for i in test_idx]

    print(f"   Train samples: {len(X_train)} | Test samples: {len(X_test)}")
    return X_train, X_test, y_train, y_test


# ==========================================
# SIMPLE KNN MODEL
# ==========================================
class SimpleKNN:
    def __init__(self, k=3):
        self.k = k
        self.X = None
        self.y = None

    def fit(self, X, y):
        self.X = X
        self.y = y

    def predict(self, X_test):
        preds = []
        for xt in X_test:
            # Calculate Euclidean distances to all training points
            distances = []
            for x in self.X:
                dist = sum((a - b) ** 2 for a, b in zip(xt, x)) ** 0.5
                distances.append(dist)

            # Get k nearest neighbors
            k_indices = sorted(range(len(distances)), key=lambda i: distances[i])[:self.k]
            k_labels  = [self.y[i] for i in k_indices]

            # Majority vote
            pred = max(set(k_labels), key=k_labels.count)
            preds.append(pred)

        return preds


# ==========================================
# SIMPLE NAIVE BAYES MODEL
# ==========================================
class SimpleNaiveBayes:
    def __init__(self):
        self.class_probs   = {}
        self.feature_probs = {}
        self.classes       = set()

    def fit(self, X, y):
        self.classes  = set(y)
        n_samples     = len(y)
        n_features    = len(X[0]) if X else 0

        for c in self.classes:
            self.class_probs[c]   = sum(1 for label in y if label == c) / n_samples
            self.feature_probs[c] = {}

            class_samples = [X[i] for i in range(n_samples) if y[i] == c]

            for feat_idx in range(n_features):
                feat_values   = [sample[feat_idx] for sample in class_samples]
                unique_values = set(feat_values)

                self.feature_probs[c][feat_idx] = {}
                for val in unique_values:
                    count = sum(1 for v in feat_values if v == val)
                    # Laplace smoothing
                    self.feature_probs[c][feat_idx][val] = (
                        (count + 1) / (len(class_samples) + len(unique_values))
                    )

    def predict(self, X_test):
        preds = []
        for xt in X_test:
            class_scores = {}

            for c in self.classes:
                score = self.class_probs[c]

                for feat_idx, feat_val in enumerate(xt):
                    if feat_val in self.feature_probs[c][feat_idx]:
                        score *= self.feature_probs[c][feat_idx][feat_val]
                    else:
                        score *= 0.01  # Small probability for unseen values

                class_scores[c] = score

            best_class = max(class_scores, key=class_scores.get)
            preds.append(best_class)

        return preds


# ==========================================
# TRAIN MODELS WITH REAL DATASET
# ==========================================
def train_models(dataset_path="disaster_dataset.csv"):
    """
    Load dataset from CSV and train both ML models.
    
    Args:
        dataset_path: path to the CSV dataset file
    
    Returns:
        knn (SimpleKNN), nb (SimpleNaiveBayes) — both trained
    """
    print("\n" + "="*60)
    print("📂 LOADING DATASET")
    print("="*60)

    X, y = load_dataset(dataset_path)
    X_train, _, y_train, _ = split_dataset(X, y, test_ratio=0.2)

    knn = SimpleKNN(k=3)
    nb  = SimpleNaiveBayes()

    knn.fit(X_train, y_train)
    nb.fit(X_train, y_train)

    print("✅ Both models trained successfully on real dataset.")
    return knn, nb


# ==========================================
# EVALUATE MODEL PERFORMANCE
# ==========================================
def evaluate_model(model, X_test, y_test, model_name="Model"):
    """
    Calculate comprehensive evaluation metrics.
    Returns accuracy, precision, recall, F1-score.
    """
    preds = model.predict(X_test)

    tp = sum(1 for p, t in zip(preds, y_test) if p == 1 and t == 1)
    tn = sum(1 for p, t in zip(preds, y_test) if p == 0 and t == 0)
    fp = sum(1 for p, t in zip(preds, y_test) if p == 1 and t == 0)
    fn = sum(1 for p, t in zip(preds, y_test) if p == 0 and t == 1)

    total     = len(y_test)
    accuracy  = (tp + tn) / total if total > 0 else 0
    precision = tp / (tp + fp)   if (tp + fp) > 0 else 0
    recall    = tp / (tp + fn)   if (tp + fn) > 0 else 0
    f1        = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    conf_matrix = [[tn, fp], [fn, tp]]

    print(f"\n{'='*50}")
    print(f"📊 {model_name} EVALUATION")
    print(f"{'='*50}")
    print(f"Accuracy:  {accuracy:.2f} ({accuracy*100:.0f}%)")
    print(f"Precision: {precision:.2f}")
    print(f"Recall:    {recall:.2f}")
    print(f"F1-Score:  {f1:.2f}")
    print(f"\nConfusion Matrix:")
    print(f"                 Predicted")
    print(f"                 Neg  Pos")
    print(f"Actual Neg      {tn:3d}  {fp:3d}")
    print(f"       Pos      {fn:3d}  {tp:3d}")

    return {
        "accuracy": round(accuracy, 2),
        "precision": round(precision, 2),
        "recall": round(recall, 2),
        "f1": round(f1, 2),
        "confusion_matrix": conf_matrix,
        "tp": tp, "tn": tn, "fp": fp, "fn": fn,
    }


# ==========================================
# COMPARE BOTH MODELS
# ==========================================
def compare_models(dataset_path="disaster_dataset.csv"):
    """
    Train on real dataset, hold out 20% for testing, compare both models.
    """
    print("\n" + "="*60)
    print("🤖 MACHINE LEARNING MODEL COMPARISON")
    print("="*60)

    X, y = load_dataset(dataset_path)
    X_train, X_test, y_train, y_test = split_dataset(X, y, test_ratio=0.2)

    knn = SimpleKNN(k=3)
    nb  = SimpleNaiveBayes()
    knn.fit(X_train, y_train)
    nb.fit(X_train, y_train)

    knn_metrics = evaluate_model(knn, X_test, y_test, "K-NEAREST NEIGHBORS (k=3)")
    nb_metrics  = evaluate_model(nb,  X_test, y_test, "NAIVE BAYES CLASSIFIER")

    print(f"\n{'='*60}")
    print("📈 MODEL COMPARISON SUMMARY")
    print(f"{'='*60}")
    print(f"{'Metric':<15} {'KNN':<12} {'Naive Bayes':<12} {'Winner':<12}")
    print(f"{'-'*51}")

    for metric in ['accuracy', 'precision', 'recall', 'f1']:
        knn_val = knn_metrics[metric]
        nb_val  = nb_metrics[metric]
        winner  = "KNN" if knn_val > nb_val else "NB" if nb_val > knn_val else "TIE"
        print(f"{metric.capitalize():<15} {knn_val:<12.2f} {nb_val:<12.2f} {winner:<12}")

    return knn_metrics, nb_metrics


# ==========================================
# PREDICTION FUNCTIONS FOR MAIN SYSTEM
# ==========================================
def predict_path_risk(knn, path, grid):
    """
    Use KNN to predict if a path is high risk.
    Returns: 0 = Safe, 1 = Dangerous
    """
    if not path:
        return 1

    risk_count  = sum(1 for x, y in path if grid[x][y] == 'R')
    path_length = len(path)

    features   = [[2 if risk_count > 3 else 1 if risk_count > 0 else 0,
                   path_length,
                   risk_count]]
    prediction = knn.predict(features)[0]
    return 0 if prediction == 1 else 1  # Invert: 1=high survival=low risk


def predict_survival(nb, patient, rescue_time_estimate):
    """
    Use Naive Bayes to predict survival probability.
    Returns: 0 = Low survival, 1 = High survival
    """
    severity_map = {"critical": 2, "moderate": 1, "minor": 0}
    severity_num = severity_map.get(patient.severity, 1)

    features   = [[severity_num, rescue_time_estimate, 1]]
    prediction = nb.predict(features)[0]
    return prediction


def get_survival_probability(patient, rescue_time):
    """
    Calculate survival probability based on patient severity and rescue time.
    Returns probability between 0 and 1.
    """
    if patient.severity == "critical":
        base_prob  = 0.4
        time_decay = 0.03
    elif patient.severity == "moderate":
        base_prob  = 0.7
        time_decay = 0.02
    else:  # minor
        base_prob  = 0.9
        time_decay = 0.01

    survival_prob = max(0.1, base_prob - rescue_time * time_decay)
    return round(survival_prob, 2)


# ==========================================
# RUN IF EXECUTED DIRECTLY
# ==========================================
if __name__ == "__main__":
    print("Training and evaluating ML models on real dataset...")
    knn_metrics, nb_metrics = compare_models("disaster_dataset.csv")

    print("\n✅ ML models ready for integration with AIDRA system!")
    print("Use train_models('disaster_dataset.csv') to get trained models for the dispatcher.")