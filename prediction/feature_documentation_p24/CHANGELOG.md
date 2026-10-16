# Changelog

## 1.1.0 — review draft, 2026-10-16

Based on public commit `f72d446a5c3d985f60c0acad47d31bb1cd0c44d8`.

- Adopt a descriptive title and consistent cohort terminology; preserve the 203-cohort history and all-1013 static-classification disclosure.
- Add `source_tier` and `first_included_tier`; retain `feature_tier` as a compatibility alias. Document tier counts and cumulative counts.
- Separate documented raw missingness from training-partition imputation. Replace blanket first-frame-NaN wording with a compatibility pointer. Mark rules absent from public notes as unspecified.
- Add a 25-channel dictionary with zero-based indices. Missing-indicator names are documentation labels.
- Resolve 120 `sequence_value` rows from numeric labels to base feature names, retaining indices in `channel_index`. Preserve all 912 input rows and underlying model/fold/group membership.
- State the actual fold-table scope: E1/M6, E2/M5, E3/M1-v2, repeat 0, folds 0–4. Clarify that the `static` branch can contain historical predictors.
- Use a direct documentation link for manuscript references. Record the source baseline separately from the unpublished draft.
- Extend standard-library validation to cross-file groups, formulas, tiers, channels, and fold scope. Refresh the dictionary byte hash and pin its Git checkout line endings to LF.

No candidate ID, canonical candidate name, numerical formula, unit, physical group, source trace, excluded feature, upstream taxonomy cutoff, fitted model, or rights statement was changed. Inherited source-audit evidence statuses were not independently re-audited against upstream code.

### Compatibility

CSV files have added columns. Consumers should read fields by header name. In `selected_features_by_model_fold.csv`, sequence-value `feature_name` is now a variable name; consumers needing the old integer must read `channel_index`. Static-branch names retain their values. The dictionary byte hash changes with documentation columns; the original frozen-registry reference hash is preserved.
