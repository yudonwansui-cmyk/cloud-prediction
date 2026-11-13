# Solar tower receiver risk-event prediction: feature dictionary and input specifications

This package documents **106 candidate tabular predictors** and a separate **11 x 25 causal sequence input** for the manuscript *Short-Horizon Prediction of Solar Tower Receiver Risk Events under Cloud Transients*.

The primary task uses **20 s of causal history** to predict a new event onset within the next **6 s**. The endpoint names are **E1: AFD risk recurrence**, **E2: Rapid local flux ramp-up**, and **E3: High power loss**. E1 excludes the initial valid AFD episode; E3 uses the clear-sky reference. These endpoints use statistical thresholds for simulated cloud-transient sequences.

## Manuscript symbols and registered fields

Start with the [manuscript-to-feature guide](manuscript_feature_mapping.md) to find **Rrec**, **rAFD**, **ploss**, **Prec**, and **rs** in this package. For example, Rrec maps to **F019**, `frame_subregion_q_mean_dt_positive_max`, in group G7, first included in T2 and represented by sequence value channel 10 (zero-based). Its nine historical summaries are F089-F097.

Fig. 3 and Eq. (1) use **rA** = `cloud_area_ratio` (F002), **Cb** = `edge_complexity` (F003), and **rmax** = `largest_component_area_ratio` (F004). The guide records their formulas and processed 800 x 800 mask definition. These are static G1/T0 tabular features without temporal value channels.

**rAFD** = `afd_violation_ratio` (F015, G6/T2), the fraction of equal-area receiver cells above their local AFD control limits; **rs** = `shading_ratio` (F009, G3/T1), the fraction of heliostats shaded. Their dedicated [rAFD](manuscript_feature_mapping.md#rafd-afd-violation-ratio) and [rs](manuscript_feature_mapping.md#rs-heliostat-field-shading-ratio) sections document equations, ratio/percentage interpretation, historical families F053-F061 and F026-F034, and sequence indices 6/18 and 0/12.

The [CSV mapping](manuscript_feature_mapping.csv) links **all 106 candidates** to manuscript symbols or feature families, stable IDs, units, tiers, operators, historical base IDs and sequence channels. The [complete coverage guide](feature_coverage_106.md) explains the four morphology classes, five A4 fields and all 81 historical summaries. The [notation-role table](manuscript_notation_roles.csv) identifies upstream fields and labels outside the registry. The symbol aliases refer to the same 106 registered candidates.

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
| A4 | T4 | Subregion-level or lag-derived variables | 5 | 106 |

The 81 A3 candidates comprise nine base variables with nine historical operators each. The actual window is specified by window_definition: recent4_mean and recent8_mean use 4 s and 8 s despite the trailing20s name suffix.

Public feature identifiers and descriptions use `subregion` for the 126 statistical receiver subregions (18 circumferential sectors x 7 axial levels). These are distinct from the 18 physical receiver panels and the finer optical/AFD receiver-cell grid. F001-F106 identify the registered fields in the 106-candidate dictionary.

## Dictionary and missingness

- **raw_missing_rule** describes feature construction before model imputation.
- **imputation_rule** describes preprocessing fitted on the training partition.
- **missing_handling** points to these two fields.

The first-frame convention for shadow_ratio_dt, newly_shaded_ratio, and newly_recovered_ratio is zero. F018-F022 are NaN at the first frame, and F023-F025 are empty raw CSV cells read as missing values. Subregion rates use the immediately preceding frame; nonfinite or nonpositive elapsed time raises an error. Historical statistics omit nonfinite observations; a window with no finite observations yields NaN, and a trend needs at least two finite observations at distinct times. The [receiver conventions](feature_formulas.md#receiver-statistics-and-index-conventions) define subregion IDs, physical locations, percentile interpolation, peak ties and invalid-input handling.

Tabular imputation/encoding and sequence channel median/mean/std are fitted on the training partition only. Sequence missing indicators use 1 for NaN and 0 for a present value; the observed-time mask uses 1 for an available aligned timepoint and 0 otherwise. See [missingness and preprocessing](sequence_input_11x25.md#missingness-and-preprocessing) for raw-statistic estimation, median filling, standardization and numerical zero padding.

## Sequence representation and fold inputs

The separate sequence representation has **11 timepoints × 25 channels**: 12 standardized values, 12 matching missing indicators, and one observed-time mask. These channels are not added to the 106 tabular candidates.

The sequence channel dictionary records zero-based indices, roles, base features, groups, and units. Labels ending in __missing and observed_time_mask are documentation labels. The base_unit field gives the physical unit before standardization.

The fold table records **repeat 0, folds 0–4**, for **E1/M6 (LSTM), E2/M5, and E3/M1**. The static branch may include historical predictors. For sequence_value rows, channel_index preserves the original index and feature_name gives the base variable name. Indicators and the time mask are not separately selected rows.

### Outer-fold input counts

The following counts are calculated from the **912 rows** of [selected_features_by_model_fold.csv](selected_features_by_model_fold.csv): **792 static** and **120 sequence-value** records. They describe the five outer-fold models in repeat 0.

| Endpoint/model and input branch | Fold 0 | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Total |
|---|---:|---:|---:|---:|---:|---:|
| E1 / M6 static | 51 | 8 | 51 | 51 | 51 | 212 |
| E1 / M6 sequence_value | 12 | 12 | 12 | 12 | 12 | 60 |
| E2 / M5 static | 52 | 52 | 52 | 52 | 52 | 260 |
| E2 / M5 sequence_value | 12 | 12 | 12 | 12 | 12 | 60 |
| E3 / M1 static | 64 | 64 | 64 | 64 | 64 | 320 |

E1 Fold 1 contains eight A0 fields in its static branch; the other four E1 static branches each contain eight A0 and 43 A3 fields. E2 static branches each contain eight A0 and 44 A3 fields. E3 static branches each contain eight A0, four A1, eight A2 and 44 A3 fields. E1/E2 each have twelve current dynamic values in the sequence branch, with no duplication of those current fields in the static branch. Historical summaries remain distinct tabular fields. Missing indicators and the observed-time mask are not separately selected rows.

E1 selected tiers **T3, T2, T3, T3, T3** for Folds 0-4, respectively. These tiers explain the different feature families present in those folds. The final E1 refit selected T2, as shown below. The fold CSV records input memberships.

### Final refit input configuration (Table 8)

This table describes the **final models fitted within the full 810-cloud development cohort**, after development-only tier selection and redundancy filtering. Counts refer to raw registered fields before categorical encoding and correspond to manuscript Table 8.

| Endpoint/model | Selected tier | Candidates in tier | After redundancy filtering | Actual tabular fields | Sequence input |
|---|---|---:|---:|---:|---|
| E1 / M6 (LSTM) | T2 | 20 | 20 | 8 | 11 x 25 |
| E2 / M5 (GRU) | T3 | 101 | 64 | 52 | 11 x 25 |
| E3 / M1 (L2 logistic regression) | T3 | 101 | 64 | 64 | none |

For M5/M6, the twelve current dynamic quantities enter the sequence branch: **20 = 8 + 12** for E1 and **64 = 52 + 12** for E2. For E3, all 64 retained fields enter the tabular model. The 25 sequence channels comprise twelve values, twelve missing indicators and one observed-time mask; they are not 25 additional registered tabular candidates.

The development cohort contains 810 clouds. **809 clouds contribute eligible E1 training anchors; all 810 contribute for E2 and E3.** One cloud has no eligible E1 anchors under the event eligibility rules.

Outer-fold models and the final refit use different training partitions and can select different tiers and retained fields. The two tables therefore describe different fitting stages.

## Files

- [manuscript_feature_mapping.md](manuscript_feature_mapping.md) and [manuscript_feature_mapping.csv](manuscript_feature_mapping.csv): manuscript symbols, representative predictors, formulas, and input locations.
- [feature_coverage_106.md](feature_coverage_106.md): complete mapping coverage, detailed families, historical operators and final-refit count interpretation.
- [manuscript_notation_roles.csv](manuscript_notation_roles.csv): upstream fields, reference quantities, labeling symbols and representations outside the 106-candidate registry.
- [feature_dictionary_106.csv](feature_dictionary_106.csv): definitions, units, tiers, timing, formulas, and missingness.
- [feature_group_mapping.csv](feature_group_mapping.csv): semantic groups.
- [feature_formulas.md](feature_formulas.md): calculations and preprocessing.
- [sequence_input_11x25.md](sequence_input_11x25.md) and [sequence_channel_dictionary_25.csv](sequence_channel_dictionary_25.csv): temporal alignment and channels.
- [selected_features_by_model_fold.csv](selected_features_by_model_fold.csv): recorded fold inputs.
- [RIGHTS.md](RIGHTS.md): rights.
