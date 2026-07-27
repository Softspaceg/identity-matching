# identity-matching

Single source of truth for matching person names and ID/passport numbers.
Shared across `ocr-pipeline` and `identity-verification` so that a change to
the matching method — the normalization rules, the similarity algorithm, the
decision threshold — happens once and takes effect in every consuming app.

**Scope: matching only, not extraction.** This package takes already-extracted
values (a name string, an ID number string, a list of candidate names) and
decides whether they match, how similar they are, or which candidate is the
best match. Pulling those values out of a document's `extracted_data` — which
fields to look at, how a merged front/back or passport shape nests them, MRZ
parsing — is specific to each app's own document schema and stays local to
that app, not here. That boundary is deliberate: the schema each app parses
can diverge over time even though the matching decision they need should not.

## Modules

- `identity_matching.name_matching` — `normalize_name`, `name_similarity`
  (fuzzy ratio, word-order insensitive), `names_match` (threshold decision),
  `best_name_match` (best-scoring candidate out of several).
- `identity_matching.id_matching` — `normalize_id_number` (validates the
  15-digit Emirates ID shape), `ids_match` (exact-match decision),
  `find_conflicting_values` (do N sources agree on one exact-match value?).

Comparison functions return `True` (match), `False` (no match), or `None`
(not enough data to decide) so callers can layer their own fallback behaviour
on top.

## Using this from another project

Not published to PyPI — install straight from this repo, pinned to a tag:

```
# requirements.txt
git+https://github.com/Softspaceg/identity-matching.git@v0.3.0
```

```toml
# pyproject.toml
dependencies = [
    "identity-matching @ git+https://github.com/Softspaceg/identity-matching.git@v0.3.0",
]
```

```bash
pip install "identity-matching @ git+https://github.com/Softspaceg/identity-matching.git@v0.3.0"
```

```python
from identity_matching.name_matching import names_match, best_name_match
from identity_matching.id_matching import ids_match

# Extraction stays in your own app -- pull the values out of your document
# shape however that shape works, then hand the plain values to this package.
is_same_person = names_match(my_extracted_name_a, my_extracted_name_b, threshold=0.85)
```

Docker images need `git` installed in the build stage for pip to clone this
(the repo is public, so no credentials are needed either locally or in CI).

## Releasing a new version

1. Bump `version` in `pyproject.toml` (and `src/identity_matching/__init__.py`).
2. Commit, then tag: `git tag -a vX.Y.Z -m "..."` and `git push origin main --tags`.
3. Bump the `@vX.Y.Z` pin in every consuming project's `requirements.txt` /
   `pyproject.toml` and reinstall — the pin is what makes upgrades explicit
   and reviewable instead of every deploy silently picking up `main`.

## Development

```bash
pip install -e ".[dev]"
pytest
```
