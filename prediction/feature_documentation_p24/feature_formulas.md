# P24 feature formulas (source checked)

All 81 historical features are computed independently within each `(cloud_id, direction)` sequence by `add_trailing_features` in `afd_py/ml_full_cohort_v3/build_phase3_prelaunch_v2.py` (257–292). For anchor `t`, H20 = finite observations with `t-20 <= t_i <= t`. The current observation is included. A missing or infinite base value is excluded from the statistic; no finite observation leaves NaN.

| Formula ID | Exact operation |
|---|---|
| H20_MEAN | arithmetic mean of H20 finite values |
| H20_STD | population standard deviation, `np.std(..., ddof=0)` |
| H20_MIN / H20_MAX | smallest / largest H20 finite value |
| H20_RANGE | max minus min |
| H20_DELTA | last finite value minus first finite value; not divided by time |
| H20_TREND | `np.polyfit(clean_times, clean, 1)[0]`; requires at least two finite values and positive time separation; physical unit per second |
| H20_RECENT4_MEAN / H20_RECENT8_MEAN | arithmetic mean of finite values in `[t-4,t]` / `[t-8,t]` seconds, including `t`; these are seconds, not counts of samples |

The base variables use exact expressions and source positions in `feature_dictionary_p24_106.csv`. In particular, `shadow_ratio_dt` uses actual adjacent `time_s` separation, `newly_shaded_ratio`/`newly_recovered_ratio` use positive/negative parts of the *net* shading-ratio change and are not rates. V2.3 panel-rate variables use the actual adjacent-frame `dt_s`, 126 panel means (18 sectors × 7 levels), and are undefined at the first frame. `P_loss=max(0,1-P_rec/P_clear)` with a 1e-12 W clear-sky denominator floor. `edge_complexity=perimeter_px²/(4π cloud_area_px)`. Values called `ratio` are dimensionless; `P_rec` is kW, flux is kW m^-2, panel flux rates are kW m^-2 s^-1.

Tabular numeric imputation and scaling, and categorical most-frequent imputation and one-hot encoding, are fitted within the training partition. Sequence transformation fits channel medians, means and standard deviations on its training partition; the 12 missing indicators and observed-time mask remain separate channels. There is no full-data imputation. The dictionary's `raw_missing_rule` distinguishes upstream construction from `imputation_rule`: the documented first-frame shading derivative/increment convention is zero, whereas panel flux rates are undefined at the first frame. Rules absent from the public source notes are marked unspecified rather than inferred.

The four direction levels are `E_to_W`, `N_to_S`, `NE_to_SW`, and `NW_to_SE`. All 1013 static masks were nonempty. The `area_class` cutoffs from their 33.333rd/66.667th percentiles are 0.284631458875 and 0.421041162625; `complexity_class` cutoffs are 2.585099753007517 and 4.32555236505013. At or below the first cutoff is small/smooth; at or below the second is medium/irregular; above it is large/complex. `fragmentation_class` is fragmented for at least four large components or a largest-component share below 0.60; otherwise multi_patch for at least two large components or share below 0.85; otherwise single_patch. The code's large-component default is 200 pixels; recounting all 1013 stored masks at 200 pixels reproduces every count. `cloud_type` combines area with fragmented/smooth/other complexity class.

`afd_violation_ratio` equals pixels above the AFD control limit divided by total receiver pixels (`afd_dynamic.py:compute_risk_maps`). Equal pixel areas make this an equal-area fraction; there is no nonuniform weighting. Peak-panel IDs are categorical indices 0–125, not continuous physical coordinates. A historical trend adds inverse seconds to the source unit.

Provenance limitation: cloud-class cutoffs were fixed using all 1013 cloud covariates before the 810/203 split. This upstream transformation was not fitted on the 810 development clouds alone. The original CLI invocation for the 200-pixel default is not separately archived, although the stored counts are reproduced exactly at 200 pixels. The local F5 audit records these checks.
