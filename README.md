# identity-matching

Single source of truth for matching person names and ID/passport numbers
extracted from identity documents (Emirates ID, passport, and similar OCR
output). Shared across `ocr-pipeline` and `identity-verification` so that a
change to the matching method — the similarity algorithm, the decision rule,
what counts as a name/ID field — happens once and takes effect in every
consuming app.

## Modules

- `identity_matching.name_matching` — name extraction from extracted_data
  dicts (`find_name_pairs`, `extract_name`, `extract_all_names`),
  normalization (`normalize_name`), and fuzzy comparison (`name_similarity`,
  `names_match`, `best_name_match`, `fields_name_match`).
- `identity_matching.id_matching` — Emirates ID and passport number
  extraction/normalization (`extract_id_number`, `extract_passport_number`,
  `normalize_id_number`).

Each function is pure (no I/O); comparison functions return `True` (match),
`False` (no match), or `None` (not enough data to decide) so callers can layer
their own fallback behaviour on top.

## Using this from another project

This isn't published to a package index yet — install it in editable mode
from its local path, or reference it directly in `requirements.txt`:

```
# requirements.txt, from a sibling project directory
-e ../identity-matching
```

```bash
pip install -e ../identity-matching
```

```python
from identity_matching.name_matching import extract_name, names_match
from identity_matching.id_matching import extract_id_number
```

Once this repo has a remote, swap the path reference for a git URL
(`identity-matching @ git+https://.../identity-matching.git@<tag>`) so
deployments don't depend on a sibling checkout on disk.

## Development

```bash
pip install -e ".[dev]"
pytest
```
