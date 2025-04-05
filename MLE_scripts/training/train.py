import argparse
import os
import sys
import pickle
import json
import logging
import pandas as pd
import time
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import warnings
# Comment these lines if you have problems with MLFlow installation
import mlflow
mlflow.autolog()

warnings.filterwarnings("ignore", message="Fontsize .* < 1.0 pt not allowed by FreeType")

# Adds the root directory to system path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(ROOT_DIR))

# Change to CONF_FILE = "settings.json" if you have problems with env variables
CONF_FILE = "settings.json"

from utils import get_project_dir, configure_logging

# Loads configuration settings from JSON
with open(CONF_FILE, "r") as file:
    conf = json.load(file)

# Defines paths
DATA_DIR = get_project_dir(conf['general']['data_dir'])
MODEL_DIR = get_project_dir(conf['general']['models_dir'])
TRAIN_PATH = os.path.join(DATA_DIR, conf['train']['table_name'])

# Initializes parser for command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--train_file", 
                    help="Specify inference data file", 
                    default=conf['train']['table_name'])
parser.add_argument("--model_path", 
                    help="Specify the path for the output model")


class DataProcessor():
    def __init__(self) -> None:
        pass

    def prepare_data(self, max_rows: int = None) -> pd.DataFrame:
        logging.info("Preparing data for training...")
        df = self.data_extraction(TRAIN_PATH)
        return df

    def data_extraction(self, path: str) -> pd.DataFrame:
        logging.info(f"Loading data from {path}...")
        return pd.read_csv(path)


class Training():
    def __init__(self) -> None:
        """
        Instead of a DecisionTreeClassifier, we will use the RandomForestClassifier 
        to integrate the top-10 predictions snippet.
        """
        self.model = RandomForestClassifier(
            n_estimators=100, 
            random_state=conf['general']['random_state'],
            max_depth=20
        )

    def run_training(self, df: pd.DataFrame, out_path: str = None) -> None:
        """
        1) Splits the data.
        2) Trains the RandomForest.
        3) Evaluates using both F1 and Top-10 accuracy.
        4) Saves the model.
        """
        logging.info("Running training...")

        features = ["Sex","Age","Height","Weight","NOC"]
        target_col =["Category"]

        X = df[features]
        X = X.astype(np.float64)

        y = df[target_col]
        logging.info(f"Features used: {features}")
        logging.info(f"Target column: {target_col}")

        # -----------------------------
        # Split data (use stratify=y if you have class labels)
        # -----------------------------
        logging.info("Splitting data into training and test sets...")
        X_train, X_valid, y_train, y_valid = train_test_split(
            X, 
            y, 
            test_size=conf['train']['test_size'], 
            random_state=42,
            stratify=y
        )

        # -----------------------------
        # Train the RandomForest model
        # -----------------------------
        start_time = time.time()
        logging.info("Training the model...")
        self.model.fit(X_train, y_train)
        end_time = time.time()
        logging.info(f"Training completed in {end_time - start_time:.2f} seconds.")


        # -----------------------------
        # Evaluate: Top-10 Accuracy
        # Only meaningful if you have multiple classes
        # -----------------------------
        self.eval_top_10_accuracy(X_valid, y_valid)

        # -----------------------------
        # Save the model
        # -----------------------------
        self.save(out_path)

    def eval_top_10_accuracy(self, X_valid: pd.DataFrame, y_valid: pd.DataFrame) -> float:
        """
        Calculates the probability predictions and checks if 
        the true class is in the top-10 predicted classes.
        """
        if len(self.model.classes_) < 10:
            logging.warning(
                "Number of classes is less than 10. Top-10 accuracy may not be meaningful."
            )

        # Get probability predictions
        proba = self.model.predict_proba(X_valid)
        top_10_preds = np.argsort(proba, axis=1)[:, -10:]  # Get top-10 indices

        # Convert class indices to labels
        class_labels = self.model.classes_
        top_10_labels = np.array([class_labels[preds] for preds in top_10_preds])

        # Ensure y_valid is in correct format
        y_valid = y_valid.squeeze().values  # Convert DataFrame/Series to NumPy array

        # Check if true category is in top-10 predictions
        correct_in_top10 = np.array([
            true_label in pred_labels
            for true_label, pred_labels in zip(y_valid, top_10_labels)
        ])

        # Compute accuracy
        top_10_accuracy = np.mean(correct_in_top10)

        print(f"Top-10 Accuracy: {top_10_accuracy:.4f}")  # Print instead of logging
        return top_10_accuracy


    def save(self, path: str) -> None:
        logging.info("Saving the model...")
        if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR)

        if not path:
            path = os.path.join(MODEL_DIR, datetime.now().strftime(conf['general']['datetime_format']) + '.pickle')
        else:
            path = os.path.join(MODEL_DIR, path)

        with open(path, 'wb') as f:
            pickle.dump(self.model, f)


def main():
    """
    Main execution function:
      1) Configures logging
      2) Reads/prepares data
      3) Trains model (including top-10 accuracy evaluation)
    """
    configure_logging()

    data_proc = DataProcessor()
    tr = Training()

    # Prepare data
    df = data_proc.prepare_data(max_rows=conf['train']['data_sample'])

    # Run training (split, train, evaluate, save)
    tr.run_training(df)


if __name__ == "__main__":
    main()
