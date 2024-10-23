import json
import os

import pandas as pd
from jieba import Tokenizer


# Define the current and parent directories
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)

# Define dataset and result paths similar to the CGS code
NMM10000_DATASET_DIR = os.path.join(PARENT_DIR, "dataset/nmm10000")
NMM10000_PRIMARY_TERM_DICT_PATH = os.path.join(
    NMM10000_DATASET_DIR, "nmm10000_primary_term_dict.json"
)
NMM10000_TEXTS_PATH = os.path.join(NMM10000_DATASET_DIR, "nmm10000_texts.csv")
NMM10000_JIEBA_RESULTS_PATH = os.path.join(
    PARENT_DIR, "results/nmm10000_jieba_results.csv"
)

# Load the primary term dictionary from the JSON file
with open(NMM10000_PRIMARY_TERM_DICT_PATH, "r", encoding="utf-8") as f:
    nmm10000_primary_term_dict = json.load(f)

# Initialize the Tokenizer and add primary terms to the dictionary
tokenizer = Tokenizer()
for term in nmm10000_primary_term_dict.keys():
    tokenizer.add_word(term)

# Read the texts from the CSV file
df_nmm10000_texts = pd.read_csv(NMM10000_TEXTS_PATH)


def extract_primary_terms(text):
    words = tokenizer.lcut(text)
    primary_terms = {}
    for word in words:
        if word in nmm10000_primary_term_dict:
            primary_terms[word] = nmm10000_primary_term_dict[word]
    return primary_terms


# Create a new column to store the extracted primary terms
df_nmm10000_texts["extracted_primary_terms"] = df_nmm10000_texts[
    "nmm_text_for_search"
].apply(lambda x: extract_primary_terms(x))

# Create a new column to store the nmm_ids of the extracted primary terms
df_nmm10000_texts["extracted_nmm_ids"] = df_nmm10000_texts[
    "extracted_primary_terms"
].apply(lambda x: list(x.values()))

# Create a new column to check if the extracted primary terms are correct
df_nmm10000_texts["correct"] = df_nmm10000_texts.apply(
    lambda x: x["expected_nmm_id"] in x["extracted_nmm_ids"], axis=1
)

# Calculate the overall accuracy
accuracy = df_nmm10000_texts["correct"].mean()
print(f"Accuracy: {accuracy:.2f}")

# Save the results to a new CSV file
columns_to_save = [
    "nmm_text_id",
    "expected_nmm_id",
    "extracted_nmm_ids",
    "correct",
]
df_nmm10000_texts[columns_to_save].to_csv(
    NMM10000_JIEBA_RESULTS_PATH,
    index=False,
)
