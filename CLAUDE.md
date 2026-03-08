normality is a performance-sensitive text normalisation library. It is a hot
path in data pipelines that process millions of entity values from sanctions
lists, PEP databases, and corporate registries.

## Performance

- This code runs on every property value in large entity graphs. Avoid
  introducing per-character Python loops where a regex or str.translate() can
  do the work.
- Prefer compiled regexes and precomputed lookup structures (frozenset, dict,
  translate tables) over inline computation.
- When changing cleaning or normalisation logic, consider benchmarking against
  a large realistic corpus before and after.

## Text and script coverage

normality must handle text (often names) and addresses in all scripts used by
world-wide official languages, with particular focus on data found in sanctions
and PEP (Politically Exposed Persons) screening:

- Latin (English, French, Spanish, Portuguese, German, Dutch, Polish, Swedish,
  Norwegian, Danish, Finnish, Estonian, Lithuanian, Hungarian, Turkish)
- Cyrillic (Russian, Ukrainian)
- Arabic
- CJK (Simplified Chinese, Japanese, Korean)

Changes to character handling, unicode normalisation, or transliteration must
be verified not to break any of these scripts.

## Python

- Generate fully-typed, minimal Python code.
- Always explicitly check `if x is None:`, not `if x:`
- Run tests using `pytest tests/`
- Run typechecking using `mypy --strict normality`
