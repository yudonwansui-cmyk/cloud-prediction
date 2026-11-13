# Solar tower receiver risk-event prediction: feature dictionary and input specifications

This repository provides the **candidate feature dictionary and causal input specifications** accompanying the manuscript *Short-Horizon Prediction of Solar Tower Receiver Risk Events under Cloud Transients*.

The manuscript studies the probability of a new receiver risk-related event onset within the next **6 s**, using the preceding **20 s** of simulated cloud-transient history:

| Endpoint | Prediction target |
|---|---|
| E1 | AFD risk recurrence |
| E2 | Rapid local flux ramp-up |
| E3 | High power loss |

These endpoints use statistical thresholds for simulated cloud-transient sequences.

E1 concerns recurrence of a high AFD-violation state after excluding the initial valid episode; E2 concerns a positive subregion-mean flux ramp; E3 concerns an instantaneous receiver-power deficit relative to the clear-sky reference.

## Find a feature from the manuscript

The key physical quantities have direct field correspondences: **rAFD (`r_AFD`) = `afd_violation_ratio` (F015)**, **rs (`r_s`) = `shading_ratio` (F009)**, and **Rrec (`R_rec`) = `frame_subregion_q_mean_dt_positive_max` (F019)**. Read the dedicated [rAFD definition](prediction/feature_documentation/manuscript_feature_mapping.md#rafd-afd-violation-ratio) and [rs definition](prediction/feature_documentation/manuscript_feature_mapping.md#rs-heliostat-field-shading-ratio), including their historical summaries and sequence channels.

| Manuscript symbol (search alias) | Registered field | Feature ID | Group | Sequence value index (zero-based) |
|---|---|---|---|---:|
| $R_{\mathrm{rec}}$ (Rrec) | `frame_subregion_q_mean_dt_positive_max` | F019 | G7 | 10 |
| $r_{\mathrm{AFD}}$ (rAFD) | `afd_violation_ratio` | F015 | G6 | 6 |
| $p_{\mathrm{loss}}$ (ploss) | `P_loss` | F014 | G4 | 5 |
| $P_{\mathrm{rec}}$ (Prec) | `P_rec` | F013 | G4 | 4 |
| $r_s$ (rs) | `shading_ratio` | F009 | G3 | 0 |
| $r_A$ (rA) | `cloud_area_ratio` | F002 | G1 | static |
| $C_b$ (Cb) | `edge_complexity` | F003 | G1 | static |
| $r_{\max}$ (rmax) | `largest_component_area_ratio` | F004 | G1 | static |

See the [manuscript-to-feature guide](prediction/feature_documentation/manuscript_feature_mapping.md) for formulas, units, the processed-mask definition behind Fig. 3, historical features, and recorded model inputs. The [machine-readable mapping](prediction/feature_documentation/manuscript_feature_mapping.csv) also covers the representative predictors in manuscript Table 5. Symbols map to the registered field names and feature IDs. The three morphology descriptors are static tabular inputs and have no value channel in the 11 x 25 tensor.

The mapping covers **all 106 candidates**, including the four morphology classes, five detailed subregion-rate/peak-location fields and 81 historical summaries. The [complete coverage guide](prediction/feature_documentation/feature_coverage_106.md) explains the link from Table 5 and Supplementary Table S1 to each feature family. The [notation-role table](prediction/feature_documentation/manuscript_notation_roles.csv) identifies upstream physical fields and future labels separately from registered inputs.

## Inputs and documentation

- **106 candidate tabular predictors**, comprising 98 numeric and 8 categorical variables before training-partition filtering and encoding.
- **Five cumulative tiers (T0-T4)**, containing 8, 12, 20, 101, and 106 registered candidates, respectively.
- A separate **11 timepoints x 25 channels** causal-history tensor: 12 numeric values, 12 matching missing indicators, and one observed-time mask. Its channels are not added to the 106 tabular candidates.
- Units, formulas, timing, missingness rules, semantic groups, and the recorded inputs for selected endpoint/model pairs in repeat-0 outer folds 0-4.

Start with the [feature documentation](prediction/feature_documentation/). The main resources are:

| Resource | Contents |
|---|---|
| [Outer-fold model input counts](prediction/feature_documentation/README.md#outer-fold-input-counts) | Five-fold branch counts for the 912 published input records |
| [Final model input configuration (Table 8)](prediction/feature_documentation/README.md#final-refit-input-configuration-table-8) | Final-refit tiers, candidate/retained counts, tabular fields and sequence inputs |
| [Complete manuscript-to-feature coverage](prediction/feature_documentation/feature_coverage_106.md) | All 106 candidates, historical families, subregion details and manuscript notation roles |
| [Candidate feature dictionary](prediction/feature_documentation/feature_dictionary_106.csv) | Definitions, units, tiers, timing, formulas, and missingness for all 106 candidates |
| [Feature formulas](prediction/feature_documentation/feature_formulas.md) | Historical operators, preprocessing, units, and cloud-class definitions |
| [Sequence input specification](prediction/feature_documentation/sequence_input_11x25.md) | Causal temporal alignment and the 11 x 25 representation |
| [Sequence channel dictionary](prediction/feature_documentation/sequence_channel_dictionary_25.csv) | Ordered value, missing-indicator, and observed-time channels |
| [Recorded fold inputs](prediction/feature_documentation/selected_features_by_model_fold.csv) | Published input memberships for the documented endpoint/model/fold scope |

The [model input tables](prediction/feature_documentation/README.md#sequence-representation-and-fold-inputs) distinguish outer-fold inputs from the final refit configuration.

[Rights](prediction/feature_documentation/RIGHTS.md)
