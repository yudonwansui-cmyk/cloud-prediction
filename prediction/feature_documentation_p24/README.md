# P24 candidate feature documentation

This package documents **106 authorized candidate table predictors** for cloud-shadow short-horizon risk prediction using 20 s of causal history and a 6 s future onset horizon. It corresponds to Supplementary Table S5. The study used 810 development clouds and a later descriptive probability test on 203 clouds that had been used in earlier research; the latter cohort must not be described as untouched.

The 106 candidates are not the features retained in every model fold. `selected_features_by_model_fold.csv` records repeat-0 outer folds, not the final 810-cloud refit. A0–A4 are source tiers, T0–T4 are cumulative training input tiers, and G1–G7 are semantic groups rather than independently manipulable causal mechanisms. The 11×25 sequence input is documented separately and does not add 25 table predictors.

Files:

- `feature_dictionary_p24_106.csv`: definitions, units, formula references, timing, and source traces for all 106 candidates.
- `feature_group_mapping_p24.csv`, `excluded_features.csv`: group mapping and the sole excluded former candidate, `normalized_sequence_time`.
- `feature_formulas.md`, `sequence_input_11x25.md`: calculation and sequence input conventions.
- `selected_features_by_model_fold.csv`, `feature_source_trace_public.csv`: fold selection and public provenance references.
- `schema_and_version.json`, `validation/`: frozen registry and dictionary hashes plus package checks.
- `RIGHTS.md`, `CITATION.md`: reuse and citation status.

No row-level cloud data, labels, predictions, fitted weights, or upstream source code are included. Run `python validation/validate_feature_dictionary.py` to recheck package consistency. Validation against the frozen registry additionally requires a local source checkout.

## Upstream classification provenance

The area and edge-complexity class cutoffs were calculated from static masks of all **1013** clouds before the 810/203 split. The 203-cohort covariates therefore participated in this pre-existing taxonomy, although no 203 event labels or predictions were used in this documentation audit. This limits a strict development-only preprocessing claim. Exact cutoffs and source formulas are in `feature_formulas.md`. The original 200-pixel CLI argument was not archived; stored component counts reproduce at the source default of 200 pixels.

## 中文说明

本包记录 P24 冻结的 106 项授权候选表格特征，以 20 秒因果历史预测未来 6 秒事件起始，对应补充材料 Table S5。810 朵云用于开发；203 朵云曾在早期研究中使用，不能称为全新未接触测试集。106 项候选不等于每折最终入模项；`selected_features_by_model_fold.csv` 仅记录 repeat 0 外折。G1–G7 为物理语义组，A0–A4 为来源层级，11×25 时序张量为另一种输入表示。本包不含逐帧数据、标签、预测或模型权重。

云面积及边界复杂度类别阈值在 810/203 划分前由全部 1013 朵云的静态掩码计算，包含 203 云的协变量。这限制了“所有预处理仅由 810 开发云拟合”的表述。
