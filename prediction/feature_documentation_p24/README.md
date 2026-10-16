# Cloud-shadow prediction: candidate feature dictionary and input specification

**Version 1.1.0 draft — proposed documentation revision.**

This package documents **106 candidate tabular predictors** for cloud-shadow short-horizon risk prediction using 20 s of causal history and a 6 s future onset horizon. P24 identifies the frozen prediction protocol.

## Cohorts

| Identifier | Cohort | Clouds |
|---|---|---:|
| development_cohort | Development cohort | 810 |
| descriptive_evaluation_cohort | Descriptive evaluation cohort | 203 |
| full_cloud_cohort | Full cloud cohort | 1013 |

The 203-cloud cohort had been used in earlier research. Its later probability evaluation must not be described as an untouched independent test.

## Feature tiers and semantic groups

The 106 candidates are registered variables before training-partition redundancy filtering and categorical encoding. They are not the features retained in every model fold or the number of encoded design-matrix columns.

- **A0–A4 (feature_tier)** identify the groups added to the feature hierarchy.
- **T0–T4** identify cumulative input tiers. **first_included_tier** records where a candidate first enters; it is eligible for every higher cumulative tier before filtering.
- **G1–G7 (physical_group)** are physical-semantic groups, not independently manipulable causal mechanisms.

| Feature tier | First included tier | Added group | Newly added | Cumulative |
|---|---|---|---:|---:|
| A0 | T0 | Cloud morphology and motion direction | 8 | 8 |
| A1 | T1 | Geometric heliostat shading | 4 | 12 |
| A2 | T2 | Current receiver state | 8 | 20 |
| A3 | T3 | Causal historical statistics | 81 | 101 |
| A4 | T4 | Panel-level or lag-derived variables | 5 | 106 |

The 81 A3 candidates comprise nine base variables with nine historical operators each. The actual window is specified by window_definition: recent4_mean and recent8_mean use 4 s and 8 s despite the trailing20s name suffix.

## Dictionary and missingness

Feature IDs, feature names, units, formulas, and group assignments retain their definitions.

- **raw_missing_rule** describes feature construction before model imputation.
- **imputation_rule** describes preprocessing fitted on the training partition.
- **missing_handling** points to these two fields.

The first-frame convention for shadow_ratio_dt, newly_shaded_ratio, and newly_recovered_ratio is zero. Panel flux rates are undefined at the first frame. First-frame missingness is specified for the recovery/drop panel IDs; behavior for frame_peak_abs_panel_id remains unspecified. Historical statistics omit nonfinite observations; no finite observation gives NaN, and a trend needs at least two finite observations at distinct times.

Tabular imputation/encoding and sequence channel median/mean/std are fitted on the training partition only.

## Sequence representation and fold inputs

The separate sequence representation has **11 timepoints × 25 channels**: 12 standardized values, 12 matching missing indicators, and one observed-time mask. These channels are not added to the 106 tabular candidates.

The sequence channel dictionary records zero-based indices, roles, base features, groups, and units. Labels ending in __missing and observed_time_mask are documentation labels. The base_unit field gives the physical unit before standardization.

The fold table records **repeat 0, folds 0–4**, for **E1/M6 (LSTM), E2/M5, and E3/M1-v2**. It does not cover all models or the final development-cohort refit. The static branch may include historical predictors. For sequence_value rows, channel_index preserves the original index and feature_name gives the base variable name. Indicators and the time mask are not separately selected rows.

## Files

- [feature_dictionary_p24_106.csv](feature_dictionary_p24_106.csv): definitions, units, tiers, timing, formulas, and missingness.
- [feature_group_mapping_p24.csv](feature_group_mapping_p24.csv): semantic groups.
- [excluded_features.csv](excluded_features.csv): the excluded former candidate and its reason.
- [feature_formulas.md](feature_formulas.md): calculations and preprocessing.
- [sequence_input_11x25.md](sequence_input_11x25.md) and [sequence_channel_dictionary_25.csv](sequence_channel_dictionary_25.csv): temporal alignment and channels.
- [selected_features_by_model_fold.csv](selected_features_by_model_fold.csv): recorded fold inputs.
- [schema_and_version.json](schema_and_version.json) and validation/: version, dictionary hash, and package checks.
- [CHANGELOG.md](CHANGELOG.md), [CITATION.md](CITATION.md), and [RIGHTS.md](RIGHTS.md): revision history, documentation link, and rights.

## Validation

From this directory, run:

    python validation/validate_feature_dictionary.py

The checker validates cross-file mappings, counts, formulas, channels, fold scope, English-only content, absence of implementation provenance, and the dictionary hash. It writes validation/validation_result.json. The root .gitattributes fixes the dictionary's checkout line endings to LF.

Validation checks documentation consistency; it does not independently reproduce feature calculations or model training. No row-level data, labels, predictions, fitted weights, or implementation code are included.

## Cloud classification

Area and edge-complexity cutoffs were calculated from all **1013** static cloud masks before the 810/203 split. The descriptive evaluation cohort's covariates therefore participated in this taxonomy. This limits a strict development-only preprocessing claim. Exact cutoffs and classification rules are in [feature_formulas.md](feature_formulas.md).

## Documentation link

Use the [feature dictionary link](https://github.com/yudonwansui-cmyk/cloud-prediction/tree/main/prediction/feature_documentation_p24) directly in the manuscript:

> The candidate feature dictionary and input specifications are available at [GitHub](https://github.com/yudonwansui-cmyk/cloud-prediction/tree/main/prediction/feature_documentation_p24).

The default-branch link will serve this revision after the pull request is merged.
