# Changelog

## 1.1.0 — 2026-10-16

- Use protocol-neutral folder names, filenames, and documentation links.
- Use English throughout the documentation, CSV files, metadata, and pull request description.
- Remove Chinese description columns and notes.
- Remove implementation paths, line references, registry references, audit labels, and the implementation trace file.
- Retain feature_tier (A0–A4) and first_included_tier (T0–T4), with cumulative counts 8/12/20/101/106.
- Separate raw missingness from training-partition imputation.
- Add the 25-channel dictionary and resolve 120 sequence-value records to variable names while retaining indices.
- Specify the recorded fold scope: E1/M6, E2/M5, and E3/M1-v2, repeat 0, folds 0–4.
- Reference the documentation directly by link.
- Validate package consistency, English-only content, and the dictionary hash.

Candidate IDs, candidate names, units, formulas, physical groups, classification rules, and all 912 recorded fold-input memberships remain unchanged.

## Compatibility

CSV consumers must use column names. Removed description and provenance columns are no longer available. Use feature_tier for A0–A4 and first_included_tier for T0–T4. In the fold table, sequence-value feature_name contains the variable name; channel_index contains the original zero-based index.
