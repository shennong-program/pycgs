# Evaluating Coreference Graph Search on the NMM10000 Dataset

## Introduction

This evaluation aims to assess the performance of the **Primary Term Extractor** included in the **Coreference Graph Search (CGS)** in extracting Natural Medicinal Material (NMM) terms and their corresponding primary terms (i.e., NMM IDs) from texts related to NMMs.

## Dataset

The dataset used for this evaluation is called **NMM10000** (`nmm10000`). The test set is constructed based on the NMM identifiers and terms defined by the [Systematic Nomenclature for Natural Medicinal Materials (SNNMM)](https://shennongalpha.westlake.edu.cn/doc/en/snnmm/) proposed by [ShennongAlpha](https://shennongalpha.westlake.edu.cn/).

This dataset includes two files:

- `nmm10000_texts.txt`
- `nmm10000_primary_term_dict.json`

### `nmm10000_texts.txt`

This file contains 10,000 NMM entities with their associated NMM identifiers and terms as defined by SNNMM. Each NMM entity in SNNMM includes four standardized NMM terms:

- NMM Systematic Name (**NMMSN**)
- NMM Systematic Chinese Name (**NMMSN-zh**)
- NMM Generic Name (**NMMGN**)
- NMM Generic Chinese Name (**NMMGN-zh**)
- **NMM ID**

For each NMM entity, we construct four texts containing these standardized NMM terms (including both Chinese and English texts). Therefore, the dataset comprises a total of **40,000** texts.

For example, the standardized NMM terms for the NMM entity with NMM ID `nmm-0001` are:

- **NMMSN**: `Artemisia annua Part-aerial`
- **NMMSN-zh**: `黄花蒿地上部`
- **NMMGN**: `Qing-hao`
- **NMMGN-zh**: `青蒿`

Using these terms, we construct the following four texts:

```text
Text 1: Artemisia annua Part-aerial is a kind of Natural Medicinal Material.
Text 2: 黄花蒿地上部是一种天然药材。
Text 3: Qing-hao is a kind of Natural Medicinal Material.
Text 4: 青蒿是一种天然药材。
```

These texts are stored in the `nmm10000_texts.txt` file, which includes the following fields:

| Field | Data Type | Description | Example |
| - | - | - | - |
| `nmm_text_id` | `str` | Unique ID for each NMM text | `nmm_t_1` |
| `lang` | `str` | Language of the NMM text (`en` for English, `zh` for Chinese) | `en` |
| `type` | `str` | Type of NMM term contained in the text (`nmmsn`, `nmmsn-zh`, etc.) | `nmmsn` |
| `nmm_text_for_search`| `str` | The text containing the NMM term | `Artemisia annua Part-aerial is a kind of Natural Medicinal Material.`|
| `expected_nmm_id` | `str` | NMM ID corresponding to the NMM term in the text | `nmm-0001` |

### `nmm10000_primary_term_dict.json`

This JSON file contains a mapping of NMM terms to their primary terms (NMM IDs) for the 10,000 NMM entities in the dataset. The structure is as follows:

```json
{
    "nmm-0001": "nmm-0001",
    "Artemisia annua Part-aerial": "nmm-0001",
    "黄花蒿地上部": "nmm-0001",
    "Qing-hao": "nmm-0001",
    "青蒿": "nmm-0001",
    ...
}
```

## Evaluation Metrics

Using the `nmm10000_primary_term_dict.json` as a reference, we evaluate the ability of CGS to correctly extract NMM terms and their corresponding primary terms/NMM IDs from the texts in `nmm10000_texts.txt`. The primary metric is the **accuracy** of NMM term extraction.

## Experiment

We compare the performance of two methods:

- **CGS**: Utilizes the Primary Term Extractor in CGS to extract NMM terms and their corresponding NMM IDs.
- **Jieba**: Employs the [Jieba](https://github.com/fxsjy/jieba) tokenizer to extract NMM terms and their corresponding NMM IDs. To ensure a fair comparison, we initialize Jieba's tokenizer with all the keys from `nmm10000_primary_term_dict.json`.

## Evaluation Code

The evaluation scripts are provided in the `scripts/` directory:

- `eval_cgs.py`: Evaluates the performance of CGS on the NMM10000 dataset.
- `eval_jieba.py`: Evaluates the performance of Jieba on the NMM10000 dataset.

## Evaluation Results

After running the evaluation scripts, the results are saved in the `results/` directory:

- `nmm10000_cgs_results.csv`: Results of CGS on the NMM10000 dataset.
- `nmm10000_jieba_results.csv`: Results of Jieba on the NMM10000 dataset.

These CSV files contain the following fields:

| Field | Data Type | Description | Example |
| - | - | - | - |
| `nmm_text_id` | `str` | Corresponds to `nmm_text_id` in `nmm10000_texts.txt` | `nmm_t_1` |
| `expected_nmm_id` | `str` | Corresponds to `expected_nmm_id` in `nmm10000_texts.txt` | `nmm-0001` |
| `extracted_nmm_id`| `list[str]` | List of NMM IDs extracted by the method. Multiple IDs may be extracted due to method variations | `['nmm-0001']` |
| `correct` | `bool` | Indicates whether the extraction is correct (`True` if `expected_nmm_id` is in `extracted_nmm_id`)| `True` |

## Final Evaluation Results

The accuracy of each method on the NMM10000 dataset is summarized below:

| Method | Accuracy |
| - | - |
| CGS | 1.00 |
| Jieba | 0.75 |
