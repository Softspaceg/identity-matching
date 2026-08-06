# matching-utils

Single source of truth for matching person names, ID/passport numbers,
alphanumeric reference codes, and descriptive free text. Shared across
`ocr-pipeline`, `asico-pm`, `identity-verification`, `identity-extraction`,
and `dld` so that a change to the matching method — the normalization rules,
the similarity algorithm, the decision threshold — happens once and takes
effect in every consuming app.

**Scope: matching only, not extraction.** This package takes already-extracted
values (a name string, an ID number string, a list of candidate names) and
decides whether they match, how similar they are, or which candidate is the
best match. Pulling those values out of a document's `extracted_data` — which
fields to look at, how a merged front/back or passport shape nests them, MRZ
parsing — is specific to each app's own document schema and stays local to
that app, not here. That boundary is deliberate: the schema each app parses
can diverge over time even though the matching decision they need should not.

## Modules

- `matching_utils.name_matching` — `normalize_name`, `name_similarity`
  (fuzzy ratio, word-order insensitive), `names_match` (threshold decision),
  `best_name_match` (best-scoring candidate out of several).
- `matching_utils.id_matching` — `normalize_id_number` (converts
  Arabic-Indic digits to Western and validates the 15-digit Emirates ID
  shape), `ids_match` (exact-match decision), `find_conflicting_values` (do
  N sources agree on one exact-match value?).
- `matching_utils.code_matching` — `normalize_code` (uppercase, strip
  whitespace/dashes/underscores; unlike `normalize_id_number`, not restricted
  to 15 digits), `codes_match` (exact-match decision) — for reference codes
  like contract numbers or unit numbers, where a one-character difference is
  a different record, not "close enough" the way a fuzzy-matched name can be.
- `matching_utils.text_matching` — `normalize_text`, `text_similarity`
  (fuzzy ratio, word-order insensitive), `texts_match` (threshold decision) —
  the same fuzzy engine as `name_matching`, for descriptive free text that
  isn't a person's name (community, building name, property type,
  nationality) and so shouldn't go through name-specific normalization
  (honorific stripping).

Comparison functions return `True` (match), `False` (no match), or `None`
(not enough data to decide) so callers can layer their own fallback behaviour
on top.

## Using this from another project

Not published to PyPI — install straight from this repo, pinned to a tag:

```
# requirements.txt
matching-utils @ git+https://github.com/Softspaceg/matching-utils.git@v1.0.0
```

```toml
# pyproject.toml
dependencies = [
    "matching-utils @ git+https://github.com/Softspaceg/matching-utils.git@v1.0.0",
]
```

```bash
pip install "matching-utils @ git+https://github.com/Softspaceg/matching-utils.git@v1.0.0"
```

```python
from matching_utils.name_matching import names_match, best_name_match
from matching_utils.id_matching import ids_match
from matching_utils.code_matching import codes_match
from matching_utils.text_matching import texts_match

# Extraction stays in your own app -- pull the values out of your document
# shape however that shape works, then hand the plain values to this package.
is_same_person = names_match(my_extracted_name_a, my_extracted_name_b, threshold=0.85)
```

> Renamed from `identity-matching` in v1.0.0 (previously imported as
> `identity_matching`). The old repo URL redirects, but every consuming
> project's pin should be updated to the new URL/name directly rather than
> relying on the redirect.

Docker images need `git` installed in the build stage for pip to clone this
(the repo is public, so no credentials are needed either locally or in CI).

## Releasing a new version

1. Bump `version` in `pyproject.toml` (and `src/matching_utils/__init__.py`).
2. Commit, then tag: `git tag -a vX.Y.Z -m "..."` and `git push origin main --tags`.
3. Bump the `@vX.Y.Z` pin in every consuming project's `requirements.txt` /
   `pyproject.toml` and reinstall — the pin is what makes upgrades explicit
   and reviewable instead of every deploy silently picking up `main`.

## Development

```bash
pip install -e ".[dev]"
pytest
```
