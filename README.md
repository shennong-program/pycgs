# Coreference-based Graph Search (CGS)

[![PyPI version](https://img.shields.io/pypi/v/pycgs.svg)](https://pypi.org/project/pycgs/)

This is the Python implementation of the CGS algorithm.

## Documentation

The documentation for `pycgs` is hosted via GitHub Pages from this repository:

- [English](https://shennong-program.github.io/pycgs/#/en/)
- [中文](https://shennong-program.github.io/pycgs/#/zh/)

The documentation source lives in `docs/` of this repository; pull requests are welcome.

### Local docs site

To preview the Docsify site from this repo:

```bash
npx docsify serve docs
```

Then open `http://localhost:3000` in your browser.

If you prefer not to use Docsify CLI, any static server works too:

```bash
python -m http.server -d docs 8000
```

Then open `http://localhost:8000`.

## Foundational CGS

```py
from pycgs import cgs

relationships = [('A', 'B'), ('B', 'C'), ('D', 'B'), ('E', 'F')]
primary_terms = cgs.foundational_cgs(relationships)

print(primary_terms)
# Output:
# {'A': 'C', 'B': 'C', 'C': 'C', 'D': 'C', 'E': 'F', 'F': 'F'}
```

## Weighted CGS

```py
from pycgs import cgs

weighted_relationships = [('A', 'B', 1), ('B', 'C', 2), ('D', 'B', 1), ('B', 'E', 1)]
primary_terms = cgs.weighted_cgs(weighted_relationships)

print(primary_terms)
# Output:
# {'A': 'C', 'B': 'C', 'C': 'C', 'D': 'C', 'E': 'E'}
```

## PrimaryTermExtractor

`PrimaryTermExtractor` is a class that allows the extraction of primary terms from a given text based on a dictionary of coreference relationships between terms and their primary terms.

```py
from pycgs.cgs import PrimaryTermExtractor

# Create a dictionary mapping terms to their primary terms
primary_term_dict = {
    "Artemisia annua Part-aerial": "nmm-0001",
    "Qing-hao": "nmm-0001",
    "黄花蒿地上部": "nmm-0001",
    "青蒿": "nmm-0001",
    "Ephedra sinica Stem-herbaceous": "nmm-0003",
    "Cao-ma-huang": "nmm-0003",
    "草麻黄草质茎": "nmm-0003",
    "草麻黄": "nmm-0003",
}

# Initialize the PrimaryTermExtractor
extractor = PrimaryTermExtractor(primary_term_dict)

# Extract primary terms from a mixed language text
text = "Both Artemisia annua Part-aerial and 草麻黄草质茎 are Natural Medicinal Materials and are used in traditional Chinese medicine."
result = extractor.extract_primary_terms(text)

print(result)
# Output:
# {'Artemisia annua Part-aerial': 'nmm-0001', '草麻黄草质茎': 'nmm-0003'}
```

## Cite this work

Yang, Z., Yin, Y., Kong, C. et al. ShennongAlpha: an AI-driven sharing and collaboration platform for intelligent curation, acquisition, and translation of natural medicinal material knowledge. Cell Discov 11, 32 (2025). <https://doi.org/10.1038/s41421-025-00776-2>
