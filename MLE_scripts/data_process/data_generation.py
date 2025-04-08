import numpy as np
import pandas as pd
import logging
import os
import sys
import json
from sklearn.model_selection import train_test_split

# Create logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define directories
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(ROOT_DIR))
from utils import singleton, get_project_dir, configure_logging

DATA_DIR = os.path.abspath(os.path.join(ROOT_DIR, '../data'))
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Change to CONF_FILE = "settings.json" if you have problems with env variables
CONF_FILE = "settings.json"

# Load configuration settings from JSON
logger.info("Loading configuration settings from JSON...")
with open(CONF_FILE, "r") as file:
    conf = json.load(file)

# Define paths
logger.info("Defining paths...")
DATA_DIR = get_project_dir(conf['general']['data_dir'])
TRAIN_PATH = os.path.join(DATA_DIR, conf['train']['table_name'])
INFERENCE_PATH = os.path.join(DATA_DIR, conf['inference']['inp_table_name'])

# Load JSON structure for event categorization
CATEGORY_JSON_PATH = "event_categories.json"
logger.info("Loading event category JSON...")
with open(CATEGORY_JSON_PATH, "r") as file:
    json_structure = json.load(file)

# Singleton class for generating sports dataset
@singleton
class SportDataGenerator():
    def __init__(self):
        self.df = None

    # Method to load and preprocess dataset
    def load_and_preprocess(self, url: str):
        logger.info("Loading dataset...")
        self.df = pd.read_csv(url)
        logger.info("Preprocessing dataset...")
        self.df = self.preprocess(self.df)
        return self.df


    # Method to preprocess dataset
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Dropping rows with missing values (excluding 'Medal')...")
        df_cleaned = df.dropna(subset=df.drop(columns="Medal").columns).copy()
        
        logger.info("Dropping unnecessary columns...")
        df_cleaned = df_cleaned.drop(columns=["Team", "Games", "Season", "City"])
        
        logger.info("Filling missing 'Medal' values with 'No Medal'...")
        df_cleaned.loc[:, 'Medal'] = df_cleaned['Medal'].fillna('No Medal')
        
        logger.info("Removing specific sports from dataset...")
        sports_to_remove = ["Motorboating", "Lacrosse", "Skeleton", "Art Competitions", "Tug-Of-War", "Rugby"]
        df_cleaned = df_cleaned[~df_cleaned['Sport'].isin(sports_to_remove)]
        
        logger.info("Identifying and removing duplicate rows...")
        duplicate_rows = df_cleaned.duplicated(subset=["Name", "Height", "Weight"], keep="first")
        df_cleaned = df_cleaned[~duplicate_rows].reset_index(drop=True)
        
        logger.info("Filtering events with less than 100 participants...")
        sport_event_counts = df_cleaned.groupby(['Sport', 'Event']).size().reset_index(name='Count')
        low_count_events = sport_event_counts[sport_event_counts['Count'] < 100]
        df_cleaned = df_cleaned[~df_cleaned['Event'].isin(low_count_events['Event'])]
        
        logger.info("Calculating unique event count...")
        unique_event_count = df_cleaned["Event"].nunique()
        logger.info(f"Unique event count: {unique_event_count}")
        
        # Flatten the JSON structure into a dictionary mapping events to categories
        event_category_map = {}
        for category, subcategories in json_structure.items():
            if isinstance(subcategories, dict):
                for subcat, events in subcategories.items():
                    for event in events:
                        event_category_map[event] = f"{category} - {subcat}"
            else:
                for event in subcategories:
                    event_category_map[event] = category
        
        logger.info("Mapping events to categories...")
        df_cleaned["Category"] = df_cleaned["Event"].map(event_category_map).fillna("Uncategorized")

        # Selecting required columns
        df_cleaned = df_cleaned[["Sex", "Age", "Height", "Weight", "NOC", "Category"]]
        
        # ------------------------------------------------------------------
        # Encoding 'Sex' and 'NOC' columns directly in df_cleaned
        # ------------------------------------------------------------------
        logger.info("Encoding 'Sex' and 'NOC' columns within preprocess...")

        # NOC için LabelEncoder
        from sklearn.preprocessing import LabelEncoder
        noc_encoder = LabelEncoder()
        
        # NOC sütunu içerisindeki verileri stringe çevirip LabelEncoder ile fit_transform
        df_cleaned["NOC"] = df_cleaned["NOC"].astype(str)
        df_cleaned["NOC"] = noc_encoder.fit_transform(df_cleaned["NOC"])
        
        # Sex sütununu map ile encode et (M -> 1, F -> 0)
        df_cleaned["Sex"] = df_cleaned["Sex"].map({"M": 1, "F": 0})
        df_cleaned["Age"] = df_cleaned["Age"].astype(float)
        df_cleaned["Height"] = df_cleaned["Height"].astype(float)
        df_cleaned["Weight"] = df_cleaned["Weight"].astype(float)

        return df_cleaned

    
    # Method to split dataset
    def split_and_save(self, df: pd.DataFrame, train_path: str, test_path: str, test_size: float = 0.2):
        logger.info("Splitting dataset into train and test sets...")
        train_df, test_df = train_test_split(df, test_size=test_size, random_state=42)
        logger.info(f"Saving train dataset to {train_path}...")
        train_df.to_csv(train_path, index=False)
        logger.info(f"Saving test dataset to {test_path}...")
        test_df.to_csv(test_path, index=False)

# Main execution
if __name__ == "__main__":
    configure_logging()
    logger.info("Starting script...")
    generator = SportDataGenerator()
    dataset_url = "https://raw.githubusercontent.com/AysenurYrr/datasets/refs/heads/main/sport/athlete_events.csv"
    df = generator.load_and_preprocess(url=dataset_url)
    generator.split_and_save(df, train_path=TRAIN_PATH, test_path=INFERENCE_PATH)
    logger.info("Script completed successfully.")
