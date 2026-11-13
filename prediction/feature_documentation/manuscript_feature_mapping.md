# Manuscript symbols and feature fields

This guide connects the notation in *Short-horizon prediction of solar tower receiver risk events under cloud transients* to the published feature dictionary. References below follow Sections 3.2, 3.3, 3.6, 4.1 and 4.3, Fig. 3, Eqs. (1), (4), (10)-(14), and Table 5 of the manuscript. Equation numbers may change between manuscript versions.

The official endpoints are **E1: AFD risk recurrence**, **E2: Rapid local flux ramp-up**, and **E3: High power loss**. The package README gives the [outer-fold input counts](README.md#outer-fold-input-counts) and [final-refit configuration](README.md#final-refit-input-configuration-table-8).

## Symbol lookup

| Manuscript symbol | Plain-text aliases | Registered field | ID | Unit | Group | First tier | Sequence value / missing indices |
|---|---|---|---|---|---|---|---|
| $R_{\mathrm{rec}}$ | Rrec, R_rec | `frame_subregion_q_mean_dt_positive_max` | F019 | kW m^-2 s^-1 | G7 | T2 | 10 / 22 |
| $r_{\mathrm{AFD}}$ | rAFD, r_AFD | `afd_violation_ratio` | F015 | dimensionless | G6 | T2 | 6 / 18 |
| $p_{\mathrm{loss}}$ | ploss, p_loss | `P_loss` | F014 | dimensionless | G4 | T2 | 5 / 17 |
| $P_{\mathrm{rec}}$ | Prec, P_rec | `P_rec` | F013 | kW | G4 | T2 | 4 / 16 |
| $r_s$ | rs, r_s | `shading_ratio` | F009 | dimensionless | G3 | T1 | 0 / 12 |
| $\mathbf{d}$ | d | `direction` | F001 | categorical | G2 | T0 | no sequence channel |
| $r_A$ | rA, r_A | `cloud_area_ratio` | F002 | dimensionless | G1 | T0 | no sequence channel |
| $C_b$ | Cb, C_b | `edge_complexity` | F003 | dimensionless | G1 | T0 | no sequence channel |
| $r_{\max}$ | rmax, r_max | `largest_component_area_ratio` | F004 | dimensionless | G1 | T0 | no sequence channel |

All channel indices are zero-based. Physical units describe the quantities before sequence standardization. Missing indicators are dimensionless. The [CSV mapping](manuscript_feature_mapping.csv) additionally covers cloud morphology, positive/negative net shading-ratio changes, maximum flux, within-subregion dispersion, and companion flux-rate variables. Rows without a symbol use verbal descriptions of the existing candidates; no additional manuscript notation is implied.

The CSV covers **all 106 registered candidates**, including each historical statistic. Its `mapping_scope` distinguishes explicit manuscript symbols, verbal representatives/companions, detailed registry members of a manuscript family, and historical summaries. The [complete coverage guide](feature_coverage_106.md) explains all five tiers and their detailed fields; the [notation-role table](manuscript_notation_roles.csv) documents upstream physical quantities, thresholds and labels outside the candidate registry.

## Cloud morphology: Fig. 3 and Eq. (1)

The three descriptors use the **processed 800 x 800 binary mask**, with cloud pixels equal to one. Section 3.2 specifies the following preprocessing:

1. Convert the 600 x 600 source segmentation mask to a Boolean mask using a grayscale threshold of 127.
2. Center it on an 800 x 800 working canvas with provisional 100-pixel margins on all four sides.
3. Extend boundary-intersecting clouds into the margins using boundary-guided completion. Regularize the exterior with signed-distance-field smoothing, binary closing, hole filling, and local corner smoothing, then restore the original 600 x 600 interior.
4. Compute the descriptors on the resulting processed mask used for cloud-motion simulation.

Let $N$ be the total processed-mask pixel count ($800\times800$), $A$ the cloud-pixel count, $P$ the one-pixel morphological perimeter, and $A_{\max}$ the area of the largest connected cloud component. Eq. (1) gives

$$
r_A=\frac{A}{N},\qquad C_b=\frac{P^2}{4\pi A},\qquad r_{\max}=\frac{A_{\max}}{A}.
$$

| Manuscript descriptor | Registered field | Definition | Fig. 3 example, 0001_GT |
|---|---|---|---:|
| $r_A$ | F002 / `cloud_area_ratio` | Cloud area divided by all processed-mask pixels | 0.208 |
| $C_b$ | F003 / `edge_complexity` | Squared morphological perimeter divided by $4\pi$ times cloud area | 6.18 |
| $r_{\max}$ | F004 / `largest_component_area_ratio` | Largest connected cloud area divided by total cloud area | 0.611 |

Fig. 3 gives the rounded example values above. All three descriptors are dimensionless, static G1 candidates first included in T0. They have no value or missing-indicator channels in the temporal tensor. The registry defines all three as zero for an empty mask; the study's 1,013 masks were nonempty.

The 600 x 600 source mask and the provisional zero-filled canvas represent intermediate stages; using either would change the descriptor values. In particular, the denominator of $r_{\max}$ is **cloud area $A$**, while that of $r_A$ is **total mask area $N$**. The prescribed 1400 m spatial mapping is a simulation scale; these descriptors do not estimate physical cloud dimensions from the source images. The feature formulas document how the descriptors feed the static cloud classes and the population used for their cutoffs.

## Rrec: maximum positive subregion flux ramp

For each fixed statistical receiver subregion $g$, first compute its mean incident flux $\bar q_g(n)$. There are $J=18\times7=126$ subregions, distinct from the 18 physical panels and the finer optical/AFD receiver-cell grid. With the recorded time interval $\Delta t_n=t_n-t_{n-1}$, Eqs. (13)-(14) define

$$
\dot q_g(n)=\frac{\bar q_g(n)-\bar q_g(n-1)}{\Delta t_n},\qquad
R_{\mathrm{rec}}(n)=\max_{1\le g\le126}\max(\dot q_g(n),0).
$$

This is exactly the physical quantity documented as **F019**, `frame_subregion_q_mean_dt_positive_max`, with formula ID `RAW_frame_subregion_q_mean_dt_positive_max`. It measures a local flux ramp, in kW m^-2 s^-1. The first frame is undefined because there is no preceding observation. Subsequent rates use actual elapsed seconds, including when they differ from the nominal 2 s interval. For a finite frame where all subregions decrease or remain unchanged, Rrec is zero.

The companion fields are F018, `frame_subregion_q_mean_dt_abs_max`, for $\max_g|\dot q_g|$, and F020, `frame_subregion_q_mean_dt_negative_magnitude_max`, for $\max_g\max(-\dot q_g,0)$. A total-power derivative has different physical units and cannot be substituted for Rrec.

### Historical Rrec predictors

The following nine fields summarize historical Rrec values. They first enter T3 and remain in G7.

| ID | Registered field | Operator |
|---|---|---|
| F089 | `frame_subregion_q_mean_dt_positive_max_mean_trailing20s` | H20_MEAN |
| F090 | `frame_subregion_q_mean_dt_positive_max_std_trailing20s` | H20_STD |
| F091 | `frame_subregion_q_mean_dt_positive_max_min_trailing20s` | H20_MIN |
| F092 | `frame_subregion_q_mean_dt_positive_max_max_trailing20s` | H20_MAX |
| F093 | `frame_subregion_q_mean_dt_positive_max_range_trailing20s` | H20_RANGE |
| F094 | `frame_subregion_q_mean_dt_positive_max_delta_trailing20s` | H20_DELTA |
| F095 | `frame_subregion_q_mean_dt_positive_max_trend_trailing20s` | H20_TREND |
| F096 | `frame_subregion_q_mean_dt_positive_max_recent4_mean_trailing20s` | H20_RECENT4_MEAN |
| F097 | `frame_subregion_q_mean_dt_positive_max_recent8_mean_trailing20s` | H20_RECENT8_MEAN |

The window includes the anchor and uses only observations from the same `(cloud_id, direction)` sequence. The last two means use the recent 4 s and 8 s, respectively. See [feature_formulas.md](feature_formulas.md) for finite-value handling, trend requirements, and units.

### Sequence and recorded model inputs

Rrec occupies value channel **10** and matching missing-indicator channel **22** in the separate 11 x 25 tensor; channel 24 is the shared observed-time mask. At each grid time, alignment selects the most recent observation at or before that time, with at most a 2 s backward gap. See the [sequence specification](sequence_input_11x25.md).

In the published [fold-input records](selected_features_by_model_fold.csv), F019 appears in all five repeat-0 folds as follows:

| Endpoint / recorded model | Input branch for current Rrec | Recorded folds |
|---|---|---|
| E1 / M6 (LSTM) | `sequence_value`, channel 10 | 0-4 |
| E2 / M5 (GRU) | `sequence_value`, channel 10 | 0-4 |
| E3 / M1 (logistic regression) | `static` (tabular) | 0-4 |

These rows describe repeat-0 outer folds. Historical summaries are separate tabular inputs.

## rs: heliostat-field shading ratio

**rs** (`r_s`, $r_s$) is **F009**, `shading_ratio`, in **G3**, first included in **T1**. It measures the fraction of heliostats shaded at the current frame, as a dimensionless ratio in [0,1].

The shading ratio in Eq. (4) is

$$
r_s(t)=1-\frac{1}{N_h}\sum_{i=1}^{N_h}w_i(t),
$$

where binary $w_i=1$ denotes an active heliostat. This maps to `shading_ratio` (F009). The fields `newly_shaded_ratio` and `newly_recovered_ratio` (F011/F012) are the positive and negative parts of the **net** adjacent shading-ratio change; they are dimensionless increments, not time derivatives. `shadow_ratio_dt` (F010) divides the net change by actual elapsed seconds.

**These features represent the positive and negative parts of the net change in the field shading ratio, rather than gross heliostat-level shading and recovery transitions.** For `delta_rs = r_s(n) - r_s(n-1)`, F011 is `max(delta_rs, 0)` and F012 is `max(-delta_rs, 0)`. Both net-change fields are zero at the first frame.

There are $N_h=2650$ heliostats in this study. All active gives rs = 0; all shaded gives rs = 1. Fig. 5's maximum-shading example has 846 shaded heliostats, so rs = 846/2650 = 0.319245... (displayed as 0.319 or 31.9%). The stored ratio is not multiplied by 100. The denominator counts heliostats; it is not cloud-mask area, receiver area, or power-weighted heliostat output.

Current rs occupies sequence value channel **0** and matching missing-indicator channel **12**. Its nine historical summaries are **F026-F034**. The additional nine summaries of its derivative `shadow_ratio_dt` are **F035-F043**. See the historical table below for the exact IDs and operators.

## Receiver power and power-loss ratio

The receiver incident power $P_{\mathrm{rec}}$ maps to `P_rec` (F013), the nonnegative receiver-flux integral reported in kW. The normalized instantaneous power deficit in Eq. (12) maps to `P_loss` (F014):

$$
p_{\mathrm{loss}}(n)=\max\left(0,1-\frac{P_{\mathrm{rec}}(n)}{P_{\mathrm{clear}}}\right).
$$

The dictionary documents a 1e-12 W floor on the clear-sky denominator. Numerator and denominator must use consistent power units. `P_loss` is a dimensionless ratio despite its capitalized field name.

## rAFD: AFD violation ratio

**rAFD** (`r_AFD`, $r_{\mathrm{AFD}}$) is **F015**, `afd_violation_ratio`, in **G6**, first included in **T2**. It is the fraction of equal-area receiver cells whose incident flux exceeds the local AFD control limit, as a dimensionless ratio in [0,1]. Eq. (10) gives

$$
r_{\mathrm{AFD}}(t)=\frac{1}{N_c}\sum_{j=1}^{N_c}
\mathbf{1}\left[q_j(t)>q_{\mathrm{AFD,ctrl},j}(t)\right],\qquad N_c=200\times503.
$$

Equal-area receiver cells make this a surface-area fraction. The strict cell-level comparison `>` is distinct from the event-level comparison `>=` below.

Equivalently, Eq. (10) first computes the cell utilization $R_j=q_j/q_{\mathrm{AFD,ctrl},j}$, then counts cells with $R_j>1$. The control limit is $q_{\mathrm{AFD,ctrl},j}=0.95q_{\mathrm{AFD,hard},j}$ under Eq. (9). The receiver has **100,600 cells**, a finer grid than the 126 subregions used by Rrec. A cell exactly at its control limit is not counted. A ratio of 0.10 means 10% of receiver area exceeds local limits; it does not mean flux is 10% above the limit.

Current rAFD occupies sequence value channel **6** and matching missing-indicator channel **18**. Its nine historical summaries are **F053-F061**. The separate **0.0786** E1 threshold is applied to this ratio to identify threshold-positive states; it is not a cell-level flux limit and rAFD itself is not the future E1-onset label. Both rs and rAFD can serve as physical inputs to more than one endpoint's model.

## Historical rAFD and rs predictors

Each historical field has the base quantity's physical group (G6 for rAFD, G3 for rs) and first enters T3. Field names use the suffix `<operator>_trailing20s` after `afd_violation_ratio_` or `shading_ratio_`:

| Operator | rAFD ID | rs ID | Meaning |
|---|---|---|---|
| `mean` | F053 | F026 | Mean of finite values in [t-20,t] |
| `std` | F054 | F027 | Population standard deviation |
| `min` | F055 | F028 | Minimum |
| `max` | F056 | F029 | Maximum |
| `range` | F057 | F030 | Maximum minus minimum |
| `delta` | F058 | F031 | Last finite value minus first finite value |
| `trend` | F059 | F032 | Least-squares slope against recorded seconds |
| `recent4_mean` | F060 | F033 | Mean in [t-4,t] |
| `recent8_mean` | F061 | F034 | Mean in [t-8,t] |

For example, F053 is `afd_violation_ratio_mean_trailing20s`, and F032 is `shading_ratio_trend_trailing20s`. Trend units are s^-1; the other eight operators remain dimensionless. All windows include the anchor, exclude nonfinite base observations, and remain within one `(cloud_id, direction)` sequence. A window with no finite observations yields a missing statistic, not zero. Trends also require at least two finite observations at distinct times. Missingness is handled separately from training-partition imputation.

In the published repeat-0 fold-input table, current rs and rAFD each appear in all five folds for E1/M6 and E2/M5 as `sequence_value` channels 0 and 6, respectively, and for E3/M1 as `static` tabular fields. The current fields' matching missing-indicator channels are 12 and 18. Historical summaries are separate tabular candidates.

## Physical inputs and event targets

Rrec, rAFD, and ploss describe physical states available up to the prediction anchor. The same types of quantities are also used by the manuscript's event-label definitions. A physical value is distinct from an event indicator or a future-onset label.

| Endpoint | Physical indicator | Manuscript statistical threshold |
|---|---|---|
| E1 | rAFD / `afd_violation_ratio` | 0.0786 (development P80) |
| E2 | Rrec / `frame_subregion_q_mean_dt_positive_max` | 19.61 kW m^-2 s^-1 (development P90) |
| E3 | ploss / `P_loss` | 0.4293 (development P80) |

Section 4.1 applies `indicator >= threshold`, requires at least two consecutive positive samples, and merges qualifying runs separated by at most one negative sample. E1 excludes the initial valid AFD episode as a prediction target. Section 4.2 requires raw-negative states at the current and two preceding frames for online eligibility. Only history through the anchor enters the predictor; future observations assign the next-6-s onset label offline.
The statistical event thresholds are development-set quantiles.

The static cloud-class cutoffs use all 1,013 mask covariates and are separate from the development-set event thresholds.
