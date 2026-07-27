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

Not published to PyPI — install straight from this repo, pinned to a tag:

```
# requirements.txt
git+https://github.com/Softspaceg/identity-matching.git@v0.1.0
```

```toml
# pyproject.toml
dependencies = [
    "identity-matching @ git+https://github.com/Softspaceg/identity-matching.git@v0.1.0",
]
```

```bash
pip install "identity-matching @ git+https://github.com/Softspaceg/identity-matching.git@v0.1.0"
```

```python
from identity_matching.name_matching import extract_name, names_match
from identity_matching.id_matching import extract_id_number
```

Docker images need `git` installed in the build stage for pip to clone this
(the repo is public, so no credentials are needed either locally or in CI).

## Releasing a new version

1. Bump `version` in `pyproject.toml`.
2. Commit, then tag: `git tag -a vX.Y.Z -m "..."` and `git push origin main --tags`.
3. Bump the `@vX.Y.Z` pin in every consuming project's `requirements.txt` /
   `pyproject.toml` and reinstall — the pin is what makes upgrades explicit
   and reviewable instead of every deploy silently picking up `main`.

## Development

```bash
pip install -e ".[dev]"
pytest
```
