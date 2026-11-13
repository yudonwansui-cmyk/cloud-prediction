# Complete manuscript-to-feature coverage

The [manuscript mapping CSV](manuscript_feature_mapping.csv) covers **all 106 registered candidates**, in stable feature-ID order. It connects the representative quantities in Table 5 and the feature families in Section 4.3 / Supplementary Table S1 to the detailed registry. Read the [symbol and formula guide](manuscript_feature_mapping.md) for Rrec and the Fig. 3 descriptors.

The package [README](README.md) gives the endpoint names and the two model-input summary tables.

## How to interpret the mapping

`paper_symbol` is populated only for the nine explicit manuscript-symbol correspondences. An empty symbol does not imply a missing feature. `mapping_scope` distinguishes four relationships:

| Scope | Interpretation |
|---|---|
| `manuscript_symbol` | A directly corresponding manuscript symbol, such as Rrec or rA |
| `manuscript_representative_or_companion` | A verbal representative in Table 5 or a documented companion quantity |
| `registry_detail_of_manuscript_family` | A detailed registered member of a manuscript feature family; the manuscript does not individually name it |
| `historical_summary_of_manuscript_quantity` | One of the 81 causal historical summaries described as a family in Section 4.3 / Table S1 |

`base_paper_symbol` identifies a related upstream symbol, not an additional predictor or an exhaustive dependency list. `dot_q_g` is a plain-text rendering of the signed subregion rate in Eq. (13); `q_j` is the cell flux in Eq. (5). `base_feature_id` connects each historical row to its registered current quantity. The operator, formula ID, window, unit, group and first tier are copied from the authoritative [feature dictionary](feature_dictionary_106.csv). Search aliases on a historical row refer to its base quantity; the blank `paper_symbol` distinguishes a derived statistic from that current quantity.

## Composition and complete coverage

| Information family | Newly added candidates | First tier | Cumulative candidates |
|---|---:|---|---:|
| A0: morphology and direction | 8 | T0 | 8 |
| A1: geometric shading | 4 | T1 | 12 |
| A2: current receiver state | 8 | T2 | 20 |
| A3: causal historical summaries | 81 | T3 | 101 |
| A4: Subregion-level or lag-derived variables | 5 | T4 | 106 |

These are candidate counts before training-fold filtering and categorical encoding. Registry order places A4 at F021-F025 and A3 at F026-F106; feature-ID order is not tier-inclusion order.

## Current, static and subregion candidates (25 fields)

The following tables identify the 25 nonhistorical fields. The 81 historical rows are covered in the next section and individually in the CSV.

### Morphology and direction: T0

| ID | Registered field | Physical meaning | Group |
|---|---|---|---|
| F001 | `direction` | Cloud-shadow propagation direction | G2 |
| F002 | `cloud_area_ratio` | Cloud-mask pixels divided by all mask pixels | G1 |
| F003 | `edge_complexity` | Squared cloud perimeter divided by 4π times cloud pixel area | G1 |
| F004 | `largest_component_area_ratio` | Largest connected component area divided by cloud area | G1 |
| F005 | `area_class` | Cloud-area class using 33.333/66.667 percentiles of 1013 masks | G1 |
| F006 | `complexity_class` | Edge-complexity class using 33.333/66.667 percentiles of 1013 masks | G1 |
| F007 | `fragmentation_class` | Fragmentation class from large-component count and largest-component share | G1 |
| F008 | `cloud_type` | Composite cloud type from area and shape classes | G1 |

F005 and F006 discretize the area and complexity descriptors. F007 uses the large-component count and largest-component share; F008 combines the morphology classes. The exact class rules and cutoffs are in [feature_formulas.md](feature_formulas.md). A component of at least 200 pixels counts as large. The class cutoffs were calculated from all 1,013 masks before splitting; the CSV references the manuscript classification family without implying that each class has its own printed symbol.

### Geometric shading: T1

| ID | Registered field | Physical meaning | Group |
|---|---|---|---|
| F009 | `shading_ratio` | Fraction of layout heliostats shaded at this frame | G3 |
| F010 | `shadow_ratio_dt` | Adjacent-frame shading-ratio change divided by elapsed seconds | G3 |
| F011 | `newly_shaded_ratio` | Positive part of adjacent net shading-ratio change | G3 |
| F012 | `newly_recovered_ratio` | Magnitude of negative adjacent net shading-ratio change | G3 |

Writing the adjacent change as `delta_rs = r_s(n) - r_s(n-1)`, F010 is `delta_rs / Delta_t_n`, F011 is `max(delta_rs, 0)`, and F012 is `max(-delta_rs, 0)`. The increments measure net shading changes, not the fraction of individual heliostats that changed state. The documented first-frame convention for these three fields is zero.

**These features represent the positive and negative parts of the net change in the field shading ratio, rather than gross heliostat-level shading and recovery transitions.**

### Current receiver state: T2

| ID | Registered field | Physical meaning | Group |
|---|---|---|---|
| F013 | `P_rec` | Receiver power from nonnegative flux integral | G4 |
| F014 | `P_loss` | Nonnegative instantaneous power loss relative to clear-sky reference | G4 |
| F015 | `afd_violation_ratio` | Receiver pixel-count fraction exceeding AFD control flux | G6 |
| F016 | `q_max` | Maximum receiver-pixel heat flux | G5 |
| F017 | `subregion_q_std_max` | Maximum within-subregion flux standard deviation | G5 |
| F018 | `frame_subregion_q_mean_dt_abs_max` | Maximum absolute adjacent-frame subregion-mean flux rate | G7 |
| F019 | `frame_subregion_q_mean_dt_positive_max` | Maximum positive adjacent-frame subregion-mean flux rate | G7 |
| F020 | `frame_subregion_q_mean_dt_negative_magnitude_max` | Maximum magnitude of negative adjacent-frame subregion-mean flux rate | G7 |

F016 is the maximum over receiver-cell fluxes, while F017 is the maximum across subregions of the within-subregion flux standard deviation. F017 does not denote the dispersion of subregion means. F018-F020 summarize the adjacent-frame rates of the 126 subregion means; their first-frame values are undefined. See the [Rrec formula](manuscript_feature_mapping.md#rrec-maximum-positive-subregion-flux-ramp) for positive, absolute and negative-magnitude summaries.

The 126 statistical subregions are formed from 18 physical receiver panels x 7 axial segments; they are distinct from the 200 x 503 optical/AFD cells.

The manuscript nomenclature uses W for receiver power and W m^-2 for cell flux; the registry reports `P_rec` in kW and flux descriptors in kW m^-2. Thus F013 is the Eq. (6) power in W divided by 1,000, and F016 is the maximum cell flux in W m^-2 divided by 1,000. Power figures may display MW. Rates retain the documented kW m^-2 s^-1 unit. Ratios remain dimensionless; multiply them by 100 only when displaying percentages.

### Subregion-level or lag-derived variables: T4

| ID | Registered field | Physical meaning | Group |
|---|---|---|---|
| F021 | `frame_subregion_q_dt_p95_abs` | 95th percentile of absolute subregion-mean flux rates | G7 |
| F022 | `frame_subregion_q_dt_std` | Population standard deviation of signed subregion-mean flux rates | G7 |
| F023 | `frame_peak_abs_subregion_id` | Subregion ID attaining the maximum absolute flux rate | G7 |
| F024 | `frame_peak_recovery_subregion_id` | Subregion ID attaining the maximum positive flux rate | G7 |
| F025 | `frame_peak_drop_subregion_id` | Subregion ID attaining the maximum negative-rate magnitude | G7 |

The A4 group, **Subregion-level or lag-derived variables**, contains F021-F025. For the signed rates in Eq. (13), F021 is the 95th percentile of their absolute values and F022 is their population standard deviation. F023, F024 and F025 identify the peaks of absolute rate, positive rate and negative-rate magnitude, respectively. These are summaries of subregion-mean rates, not cell-flux percentiles.

Peak IDs are categorical values 0-125, with `id = 18*level + sector` for zero-based axial level and circumferential sector; the manuscript index is `g = id + 1`. F021 uses linear percentile interpolation, and tied peaks select the smallest ID. An all-zero rate array selects ID 0. F018-F025 are missing at the first frame, including all three peak IDs; nonfinite or nonpositive adjacent time differences raise an error. The [receiver statistics and index conventions](feature_formulas.md#receiver-statistics-and-index-conventions) give the pixel-to-subregion mapping, physical orientation, nonfinite-input behavior and exact reduction rules. None of F021-F025 has a value channel in the 11 x 25 tensor.

## Historical summaries: nine bases x nine operators (81 fields)

All historical candidates first enter T3. The CSV contains an individual row for every one, including its base feature ID, window, operator and formula ID. These are the nine base families:

| Base ID | Base field | Manuscript connection | Historical IDs | Group |
|---|---|---|---|---|
| F009 | `shading_ratio` | r_s | F026-F034 | G3 |
| F010 | `shadow_ratio_dt` | Adjacent-time derivative of r_s | F035-F043 | G3 |
| F014 | `P_loss` | p_loss | F044-F052 | G4 |
| F015 | `afd_violation_ratio` | r_AFD | F053-F061 | G6 |
| F016 | `q_max` | Maximum receiver-cell flux (Table 5 G5) | F062-F070 | G5 |
| F017 | `subregion_q_std_max` | Subregion flux dispersion (Table 5 G5) | F071-F079 | G5 |
| F018 | `frame_subregion_q_mean_dt_abs_max` | Maximum absolute signed rate from Eq. (13) | F080-F088 | G7 |
| F019 | `frame_subregion_q_mean_dt_positive_max` | Rrec | F089-F097 | G7 |
| F020 | `frame_subregion_q_mean_dt_negative_magnitude_max` | Negative flux slopes (Table 5 G7) | F098-F106 | G7 |

Within each ID range, the operators follow this order:

| Offset | Operator | Window and meaning |
|---:|---|---|
| 0 | `mean` | Arithmetic mean over finite values in [t-20,t] |
| 1 | `std` | Population standard deviation over the same window |
| 2 | `min` | Minimum |
| 3 | `max` | Maximum |
| 4 | `range` | Maximum minus minimum |
| 5 | `delta` | Last finite value minus first finite value; not divided by time |
| 6 | `trend` | Least-squares slope against recorded seconds |
| 7 | `recent4_mean` | Mean of finite values in [t-4,t] |
| 8 | `recent8_mean` | Mean of finite values in [t-8,t] |

For example, F032 is the historical trend of r_s, F051 the recent-4-s mean of p_loss, and F095 the historical trend of Rrec. A trend adds inverse seconds to the base unit: F095 has unit kW m^-2 s^-2. All windows include the anchor and stay within a single `(cloud_id, direction)` sequence. A window containing no finite observations yields a missing value; a trend additionally needs two finite observations with distinct times. See [feature_formulas.md](feature_formulas.md) for the full historical operators and preprocessing rules.

The dictionary has no registered nine-summary family for `P_rec`, the two net shading increments, the morphology fields or the A4 fields. Their absence from the historical table follows the registry. Historical summaries do not create additional temporal value channels.

## Other manuscript symbols and the separate sequence representation

The [notation-role table](manuscript_notation_roles.csv) records upstream fields, references, labels and representations that readers may also look for. For example, `q_j` supplies F013/F016/F017 and the AFD comparison; `bar_q_g` and `dot_q_g` supply the subregion-rate fields; `P_clear` normalizes F014; and the cell-level AFD limit and utilization `R_j` construct F015. These quantities are not separately registered scalar candidates. In particular, the utilization `R_j` and ramp indicator Rrec are different physical quantities.

The raw event states `I_r`, trigger parameters `theta_r`, and future-onset labels `y_E1`, `y_E2`, `y_E3` belong to labeling and eligibility. They are not added to the causal feature vector. `x_stat` and `X_seq` name representations. The 12 sequence value channels correspond exactly to F009-F020; the 12 missing indicators and observed-time mask are representation channels, not additional tabular candidates. The CSV records channel indices only for current values, leaving historical/static/A4 fields blank. Read the [sequence specification](sequence_input_11x25.md) for alignment and channel order.

## Candidate coverage and fitted-model inputs

Mapping all 106 candidates does not imply that every model uses every candidate. The package README presents both the [outer-fold input counts](README.md#outer-fold-input-counts) and the [final-refit configuration from Table 8](README.md#final-refit-input-configuration-table-8), with their distinct fitting stages and counting conventions.

The [field-level fold inputs](selected_features_by_model_fold.csv) describe repeat-0 outer folds 0-4. The two summary tables distinguish these outer-fold models from the final refit.
