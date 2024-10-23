import json
import os

import pandas as pd

from pycgs.cgs import PrimaryTermExtractor

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
NMM10000_DATASET_DIR = os.path.join(PARENT_DIR, "dataset/nmm10000")

NMM10000_PRIMARY_TERM_DICT_PATH = os.path.join(
    NMM10000_DATASET_DIR, "nmm10000_primary_term_dict.json"
)
NMM10000_TEXTS_PATH = os.path.join(NMM10000_DATASET_DIR, "nmm10000_texts.csv")

NMM10000_CGS_RESULTS_PATH = os.path.join(PARENT_DIR, "results/nmm10000_cgs_results.csv")

# Load the primary term dictionary from the JSON file
with open(NMM10000_PRIMARY_TERM_DICT_PATH, "r", encoding="utf-8") as f:
    nmm10000_primary_term_dict = json.load(f)

# Initialize the PrimaryTermExtractor
extractor = PrimaryTermExtractor(nmm10000_primary_term_dict)


df_nmm10000_texts = pd.read_csv(NMM10000_TEXTS_PATH)


# create a new column to store the extracted primary terms
df_nmm10000_texts["extracted_primary_terms"] = df_nmm10000_texts[
    "nmm_text_for_search"
].apply(lambda x: extractor.extract_primary_terms(x))

# create a new column to store the nmm_ids of the extracted primary terms
df_nmm10000_texts["extracted_nmm_ids"] = df_nmm10000_texts[
    "extracted_primary_terms"
].apply(lambda x: list(x.values()))

# create a new column to check if the extracted primary terms are correct, if expected_nmm_id is in extracted_nmm_ids, then it is correct
df_nmm10000_texts["correct"] = df_nmm10000_texts.apply(
    lambda x: x["expected_nmm_id"] in x["extracted_nmm_ids"], axis=1
)

# calculate the accuracy
accuracy = df_nmm10000_texts["correct"].mean()
print(f"Accuracy: {accuracy:.2f}")


# save the results to a new CSV file
columns_to_save = [
    "nmm_text_id",
    "expected_nmm_id",
    "extracted_nmm_ids",
    "correct",
]
df_nmm10000_texts[columns_to_save].to_csv(
    os.path.join(CURRENT_DIR, NMM10000_CGS_RESULTS_PATH),
    index=False,
)
