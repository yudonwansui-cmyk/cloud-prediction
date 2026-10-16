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
9. `panel_q_std_max`
10. `frame_panel_q_mean_dt_abs_max`
11. `frame_panel_q_mean_dt_positive_max`
12. `frame_panel_q_mean_dt_negative_magnitude_max`

The 106 candidate tabular features and these 25 tensor channels are different representations; 25 is not added to 106. The sequence models also have a static branch. Channel median/mean/std are estimated on the training partition only. First-frame derivatives may remain missing despite an observed timepoint.

## Machine-readable channel mapping

`sequence_channel_dictionary_25.csv` documents every channel using **zero-based indices**:

| Indices | Role | Order |
|---|---|---|
| 0–11 | Standardized numeric value | The 12 variables listed above, in that order |
| 12–23 | Matching missing indicator | Same variable order; index = value index + 12 |
| 24 | Observed-time mask | Availability of an aligned observation |

`channel_name` values for indicators (`<base>__missing`) and the time mask are documentation labels, not implementation variable names. `base_feature_name` joins value/indicator channels to the 106-candidate dictionary. `channel_unit` describes the transformed channel; `base_unit` is the original physical unit. The time mask has no base-feature or physical-group assignment. This revision documents the roles without introducing a new mask coding convention.

The list above is numbered 1–12 for reading; the CSV indices are 0–11. In `selected_features_by_model_fold.csv`, `sequence_value` rows retain their original zero-based index in `channel_index` and use the base variable name in `feature_name`. That file records the value channels for selected endpoint/model pairs, not separately selected indicator or mask rows.
