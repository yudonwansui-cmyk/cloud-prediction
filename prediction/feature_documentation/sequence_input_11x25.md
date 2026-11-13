# 11 × 25 sequence input

The 11 offsets are −20, −18, …, 0 seconds relative to anchor `t`. At each offset, the cache uses the most recent observed frame no later than that grid time, allowing at most a 2 s backward gap. No future frame is used.

The ordered 25 channels are 12 standardized values, the matching 12 missing indicators, and one observed-time mask. The numeric channel order is:

1. `shading_ratio`
2. `shadow_ratio_dt`
3. `newly_shaded_ratio`
4. `newly_recovered_ratio`
5. `P_rec`
6. `P_loss`
7. `afd_violation_ratio`
8. `q_max`
9. `subregion_q_std_max`
10. `frame_subregion_q_mean_dt_abs_max`
11. `frame_subregion_q_mean_dt_positive_max`
12. `frame_subregion_q_mean_dt_negative_magnitude_max`

The 106 candidate tabular features and these 25 tensor channels are different representations; 25 is not added to 106. The sequence models also have a static branch. Channel median/mean/std are estimated on the training partition only. First-frame derivatives may remain missing despite an observed timepoint.

Causal grid alignment uses no observation later than its grid time, and every grid time is at or before the anchor. Histories remain within a single `(cloud_id, direction)` sequence. The 6 s future interval assigns offline onset labels only. `normalized_sequence_time` remains excluded because it depends on the completed sequence's `time_end_s`, which is not available at the anchor.

## Machine-readable channel mapping

Manuscript notation: **Rrec** = `frame_subregion_q_mean_dt_positive_max` (value index 10, missing-indicator index 22); **rAFD** = `afd_violation_ratio` (6/18); **ploss** = `P_loss` (5/17); **Prec** = `P_rec` (4/16); **rs** = `shading_ratio` (0/12). See the [manuscript-to-feature guide](manuscript_feature_mapping.md) for formulas and the [CSV mapping](manuscript_feature_mapping.csv) for other representative variables. These are aliases for the existing channels.

**rAFD and rs are distinct physical signals.** rAFD describes the receiver surface fraction exceeding local AFD limits; rs describes the heliostat-field fraction shaded. Both are stored as ratios before standardization. Their historical summaries are separate tabular candidates and are not inserted as extra sequence channels. The guide contains dedicated [rAFD](manuscript_feature_mapping.md#rafd-afd-violation-ratio) and [rs](manuscript_feature_mapping.md#rs-heliostat-field-shading-ratio) definitions.

`sequence_channel_dictionary_25.csv` documents every channel using **zero-based indices**:

| Indices | Role | Order |
|---|---|---|
| 0–11 | Standardized numeric value | The 12 variables listed above, in that order |
| 12–23 | Matching missing indicator | Same variable order; index = value index + 12 |
| 24 | Observed-time mask | Availability of an aligned observation |

`channel_name` values for indicators (`<base>__missing`) and the time mask are documentation labels, not implementation variable names. `base_feature_name` joins value/indicator channels to the 106-candidate dictionary. `channel_unit` describes the transformed channel; `base_unit` is the original physical unit. The time mask has no base-feature or physical-group assignment.

The list above is numbered 1–12 for reading; the CSV indices are 0–11. In `selected_features_by_model_fold.csv`, `sequence_value` rows retain their original zero-based index in `channel_index` and use the base variable name in `feature_name`. That file records the value channels for selected endpoint/model pairs, not separately selected indicator or mask rows.

## Missingness and preprocessing

Alignment is performed within each `(cloud_id, direction)` sequence sorted by `(time_s, frame_id)`. For each grid time, `searchsorted(..., side="right") - 1` selects the latest frame no later than that time. A backward gap of exactly 2 s is allowed; gap comparisons use a `1e-12` s numerical tolerance. If no eligible frame exists, all twelve aligned raw values are NaN and the timepoint is unavailable. Alignment does not interpolate between frames or choose a later observation.

| Channel role | Value 1 | Value 0 |
|---|---|---|
| Missing indicator, indices 12-23 | Corresponding aligned raw value is NaN | Corresponding aligned raw value is not NaN |
| Observed-time mask, index 24 | A frame satisfies the alignment rule | No frame satisfies the alignment rule |

The missing test is `np.isnan`, not a general nonfinite-value test. An available timepoint can still contain a missing value: the first-frame subregion rates are undefined, so their missing indicators are 1 while the observed-time mask is 1. At an unavailable timepoint, all twelve missing indicators are 1 and the observed-time mask is 0. First-frame shading derivatives and net shading increments use their construction-time zero convention; see the [feature formulas](feature_formulas.md#receiver-statistics-and-index-conventions) for subregion-rate and peak-ID conventions.

The transformation order is:

1. Construct aligned raw values and generate the missing indicators and observed-time mask before filling or scaling.
2. Estimate each value channel's median, mean and population standard deviation from the raw training-partition window tensor, pooling training windows and all eleven positions with `np.nanmedian`, `np.nanmean` and `np.nanstd(..., ddof=0)`. These functions omit NaNs; statistics are calculated before median filling. Repeated observations contribute each time they occur in training windows. Evaluation windows do not contribute. Replace a nonfinite median or mean with 0, and a nonfinite or at-most-`1e-12` standard deviation with 1.
3. Fill NaNs with the fitted channel median, then apply `(filled_value - raw_training_mean) / raw_training_std` using the statistics and fallbacks from step 2. An observed but missing value need not become zero after this transformation.
4. Set all twelve numerical channels to zero wherever the observed-time mask is 0. Preserve the missing indicators and time mask from step 1, and concatenate twelve values, twelve indicators and the time mask as `float32`. Binary channels are not standardized.

The documented layout is time by channel, `11 x 25`; model tensors store the same values as `(batch, 25, 11)`.

