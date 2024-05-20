# Coreference-based Graph Search (CGS)

[![PyPI version](https://img.shields.io/pypi/v/pycgs.svg)](https://pypi.org/project/pycgs/)

This is the Python implementation of the CGS algorithm.

## Documentation

The documentation for `pycgs` is available on the documentation website of the ShennongAlpha ([ShennongDoc](https://shennongalpha.westlake.edu.cn/doc/)):

- [English](https://shennongalpha.westlake.edu.cn/doc/en/pycgs/)
- [中文](https://shennongalpha.westlake.edu.cn/doc/zh/pycgs/)

You can also contribute to the documentation on the [`ShennongDoc`](https://github.com/Shennong-Program/ShennongDoc) GitHub repository by submitting a pull request:

- [English](https://github.com/Shennong-Program/ShennongDoc/tree/main/doc/en/pycgs/)
- [中文](https://github.com/Shennong-Program/ShennongDoc/tree/main/doc/zh/pycgs/)

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

## Cite this work

```bibtex
@misc{yang2024shennongalpha,
      title={ShennongAlpha: an AI-driven sharing and collaboration platform for intelligent curation, acquisition, and translation of natural medicinal material knowledge}, 
      author={Zijie Yang and Yongjing Yin and Chaojun Kong and Tiange Chi and Wufan Tao and Yue Zhang and Tian Xu},
      year={2024},
      eprint={2401.00020},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```
