# 11 × 25 sequence input

Source: `afd_py/ml_full_cohort_v3/run_phase3_p5_tcn.py` (`DYNAMIC_CHANNELS`, `GRID_OFFSETS`, `sequence_transform`) and P24 C1a temporal cache. The 11 offsets are −20, −18, …, 0 seconds relative to anchor `t`. At each offset, the cache uses the most recent observed frame no later than that grid time, allowing at most a 2 s backward gap. No future frame is used.

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

The 106 candidate table features and these 25 tensor channels are different representations; 25 is not added to 106. The sequence models also have a static branch. Channel median/mean/std are estimated on the training partition only. First-frame derivatives may remain missing despite an observed timepoint.
