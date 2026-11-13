# Feature formulas

The official endpoints are **E1: AFD risk recurrence**, **E2: Rapid local flux ramp-up**, and **E3: High power loss**.

## Manuscript notation

The manuscript's **Rrec** (`R_rec`) is `frame_subregion_q_mean_dt_positive_max` (F019, G7): the maximum positive adjacent-frame rate of the 126 subregion mean fluxes, using actual elapsed seconds, in kW m^-2 s^-1. It is undefined at the first frame. Its nine historical summaries are F089-F097; sequence value/missing-indicator indices are 10/22 (zero-based).

Other central correspondences are **rAFD** = `afd_violation_ratio`, **ploss** = `P_loss`, **Prec** = `P_rec`, and **rs** = `shading_ratio`. See the [manuscript-to-feature guide](manuscript_feature_mapping.md) for the equations, physical definitions, and the distinction between input quantities and future event-onset labels, and the [CSV mapping](manuscript_feature_mapping.csv) for stable feature IDs and channel indices.

The Fig. 3 morphology symbols are **rA** (`r_A`) = `cloud_area_ratio` (F002), **Cb** (`C_b`) = `edge_complexity` (F003), and **rmax** (`r_max`) = `largest_component_area_ratio` (F004). Eq. (1) defines them as `A/N`, `P^2/(4*pi*A)`, and `A_max/A` on the boundary-completed, smoothed 800 x 800 mask with the original interior restored. Here `N` counts all processed-mask pixels, `A` counts cloud pixels, `P` is the one-pixel morphological perimeter, and `A_max` is the largest connected cloud-component area. See the guide's [morphology section](manuscript_feature_mapping.md#cloud-morphology-fig-3-and-eq-1) for preprocessing and the rounded manuscript example.

## Historical operators and preprocessing

For dedicated current-value formulas, see [rAFD / F015](manuscript_feature_mapping.md#rafd-afd-violation-ratio) and [rs / F009](manuscript_feature_mapping.md#rs-heliostat-field-shading-ratio). Their nine historical operators below map to F053-F061 and F026-F034, respectively. The [complete coverage guide](feature_coverage_106.md) identifies all nine historical base families and the five A4 fields (subregion-level or lag-derived variables).

The construction of all 81 historical features is independent within each `(cloud_id, direction)` sequence. For anchor `t`, H20 = finite observations with `t-20 <= t_i <= t`. The current observation is included; observations after the anchor are excluded. A missing or infinite base value is excluded from the statistic; a window containing no finite observations yields NaN.

| Formula ID | Exact operation |
|---|---|
| H20_MEAN | arithmetic mean of H20 finite values |
| H20_STD | population standard deviation, `np.std(..., ddof=0)` |
| H20_MIN / H20_MAX | smallest / largest H20 finite value |
| H20_RANGE | max minus min |
| H20_DELTA | last finite value minus first finite value; not divided by time |
| H20_TREND | `np.polyfit(clean_times, clean, 1)[0]`; requires at least two finite values and positive time separation; physical unit per second |
| H20_RECENT4_MEAN / H20_RECENT8_MEAN | arithmetic mean of finite values in `[t-4,t]` / `[t-8,t]` seconds, including `t`; these are seconds, not counts of samples |

Base-variable definitions and units are listed in the feature dictionary. In particular, `shadow_ratio_dt` uses actual adjacent `time_s` separation, `newly_shaded_ratio`/`newly_recovered_ratio` use positive/negative parts of the *net* shading-ratio change and are not rates. Subregion-rate variables use the actual adjacent-frame `dt_s`, 126 subregion means (18 sectors × 7 levels), and are undefined at the first frame. `P_loss=max(0,1-P_rec/P_clear)` with a 1e-12 W clear-sky denominator floor. `edge_complexity=perimeter_px²/(4π cloud_area_px)`. Values called `ratio` are dimensionless; `P_rec` is kW, flux is kW m^-2, subregion flux rates are kW m^-2 s^-1.

For F011 and F012, `delta_rs = r_s(n) - r_s(n-1)`, F011 is `max(delta_rs, 0)` and F012 is `max(-delta_rs, 0)`. **These features represent the positive and negative parts of the net change in the field shading ratio, rather than gross heliostat-level shading and recovery transitions.** Both fields are zero at the first frame. A stable aggregate shading ratio can coexist with simultaneous shading and recovery of different heliostats; both net-change fields would then be zero under these definitions.

## Receiver statistics and index conventions

The 18 physical receiver panels, 126 statistical subregions (18 x 7), and 200 x 503 receiver flux/AFD cells are distinct partitions. F017 is the maximum across subregions of the pixel-flux standard deviation within each subregion. F018-F020 first average flux within each subregion, divide adjacent-frame changes by actual elapsed seconds, and summarize the absolute, positive and negative-magnitude rates. F021 is the P95 of absolute rates over the 126 subregions; F022 is the population standard deviation of their signed rates. F023-F025 are categorical peak-location IDs.

### Subregion IDs and physical locations

For a flux array with `R` rows and `C` columns, zero-based pixel coordinates `(r, c)` map to `sector = floor(18*c/C)`, `level = floor(7*r/R)`, and `id = 18*level + sector`. Sectors run from 0 to 17 and levels from 0 to 6. The inverse mapping is `sector = id % 18`, `level = id // 18`; the manuscript's mathematical index is `g = id + 1`. The subregion mean is the sum of its pixel fluxes divided by its actual pixel count, then divided by 1,000 to convert W m^-2 to kW m^-2. Each of the 126 subregions must contain pixels; otherwise construction raises an error.

The array uses a south-cut circumferential ordering: column centers have angle `-180 + 360*(c+0.5)/C` degrees, with 0 degrees at north and the two edges at the south cut. Rows increase from the receiver bottom to its top; for receiver height `H`, row-center height relative to the midplane is `-H/2 + H*(r+0.5)/R`. Thus ID 0 is sector 0 at the lowest level, IDs 0-17 span that level, and IDs 108-125 span the highest level. Discrete pixel counts can differ between subregions. These IDs specify spatial bins, not heat-transfer fluid-flow order.

### Adjacent-frame rates, percentiles and peak IDs

Frames are sorted by `(time_s, frame_id)` within each `(cloud_id, direction)` sequence. Each rate uses the immediately preceding frame's subregion means and `dt_s = time_s - previous_time_s`; it does not search backward past a missing value. A nonfinite or nonpositive `dt_s` raises an error. Flux arrays must be two-dimensional and keep the first frame's shape; parsing and shape errors stop construction.

At the first frame, F018-F022 are NaN and F023-F025 are empty raw CSV cells, read as missing values before model preprocessing. None of these first-frame quantities is assigned a zero rate or ID 0. Subsequent reductions use ordinary `np.max`, `np.quantile`, `np.std` and `np.argmax` on the 126 rates, without filtering nonfinite subregions, interpolation across invalid adjacent records, or replacement by zero. Finite flux arrays are the domain of the rate and peak-location definitions; nonfinite inputs can propagate into reductions and do not define a physical peak location.

F021 uses `np.quantile(abs(rates), 0.95)` with linear interpolation. For the sorted 126 absolute rates `a[0]` through `a[125]`, the quantile position is `125*0.95 = 118.75`, giving `0.25*a[118] + 0.75*a[119]`. F022 uses `np.std(rates, ddof=0)` over all 126 signed rates.

F023-F025 use `np.argmax` on absolute rates, positive parts `max(rate, 0)`, and negative magnitudes `max(-rate, 0)`, respectively. Ties select the smallest subregion ID. An all-zero array selects ID 0; in particular, F024 is 0 when there is no positive rate, and F025 is 0 when there is no negative rate. An ID alone therefore does not establish a ramp event. IDs remain categorical values 0-125.

## Units and preprocessing

The manuscript's W-valued receiver power converts to `P_rec` in kW by dividing by 1,000, and to displayed MW by dividing W by 1,000,000. Thus 1 MW = 1,000 kW = 1,000,000 W. W m^-2 converts to kW m^-2 by dividing by 1,000. Rates are kW m^-2 s^-1; historical trends of those rates are kW m^-2 s^-2. Other historical operators retain the base unit. Ratios are dimensionless; a plotted percentage equals 100 times the stored ratio. The 1e-12 W denominator floor corresponds to 1e-15 kW if the entire power-ratio computation is expressed in kW.

Tabular numeric imputation and scaling, and categorical most-frequent imputation and one-hot encoding, are fitted within the training partition. Sequence transformation fits channel medians, means and standard deviations on its training partition; the 12 missing indicators and observed-time mask remain separate channels. There is no full-data imputation. The dictionary's `raw_missing_rule` distinguishes feature construction from `imputation_rule`: the first-frame shading derivative/increment convention is zero, whereas subregion flux rates are undefined at the first frame.

Sequence missing indicators are generated from raw aligned values using `np.isnan` before filling or standardization: 1 means missing and 0 means present. The observed-time mask is 1 for an available aligned timepoint and 0 otherwise. Training-partition channel statistics are calculated on the raw window tensor, then NaNs are filled with the channel median and values are standardized using the raw channel mean and population standard deviation. Numerical channels at unavailable timepoints are then set to zero. See the [sequence preprocessing specification](sequence_input_11x25.md#missingness-and-preprocessing) for the order, fallback values and mask examples.

## Static cloud classes

The four direction levels are `E_to_W`, `N_to_S`, `NE_to_SW`, and `NW_to_SE`. All 1013 static masks were nonempty. The `area_class` cutoffs from their 33.333rd/66.667th percentiles are 0.284631458875 and 0.421041162625; `complexity_class` cutoffs are 2.585099753007517 and 4.32555236505013. At or below the first cutoff is small/smooth; at or below the second is medium/irregular; above it is large/complex. `fragmentation_class` is fragmented for at least four large components or a largest-component share below 0.60; otherwise multi_patch for at least two large components or share below 0.85; otherwise single_patch. A large component contains at least 200 pixels. `cloud_type` combines area with fragmented/smooth/other complexity class.

`afd_violation_ratio` equals pixels above the AFD control limit divided by total receiver pixels. Equal pixel areas make this an equal-area fraction; there is no nonuniform weighting. Peak-subregion IDs are categorical indices 0–125, not continuous physical coordinates. A historical trend adds inverse seconds to the base unit.

The cloud-class cutoffs use all 1013 cloud covariates before the 810/203 split.
