# Cloud-shadow prediction: candidate feature dictionary and input specification

**Version 1.1.0 draft — proposed documentation revision; not a released version.**

This package documents **106 authorized candidate tabular predictors** for cloud-shadow short-horizon risk prediction using 20 s of causal history and a 6 s future onset horizon. P24 is the internal identifier of the frozen prediction protocol. This package is a feature dictionary and input specification; no row-level research dataset is distributed.

## Cohort terminology

Use these terms consistently in the manuscript and documentation. They describe the roles already disclosed in the public package; they do not change cohort membership or establish independence.

| Identifier | English label | 中文名称 | Clouds |
|---|---|---|---:|
| `development_cohort` | development cohort | 开发队列 | 810 |
| `descriptive_evaluation_cohort` | descriptive evaluation cohort | 描述性评估队列 | 203 |
| `full_cloud_cohort` | full cloud cohort | 全部云样本队列 | 1013 |

The 203-cloud descriptive evaluation cohort had been used in earlier research. Its later probability evaluation must not be described as an untouched independent test. The full cloud cohort comprises the 810 and 203 clouds.

## Feature tiers and semantic groups

The 106 candidates are registered variables before training-partition redundancy filtering and categorical encoding. They are not the features retained in every model fold, and the count is not the number of encoded design-matrix columns.

- **A0–A4 (`source_tier`)** identify each candidate's source tier. The legacy `feature_tier` column remains an identical compatibility alias.
- **T0–T4** identify cumulative input tiers. `first_included_tier` states where a candidate first enters; it is also eligible for every higher cumulative tier, before filtering.
- **G1–G7 (`physical_group`)** are physical-semantic groups, not independently manipulable causal mechanisms.

| Source tier | First included tier | Added group | Newly added | Cumulative |
|---|---|---|---:|---:|
| A0 | T0 | Cloud morphology and motion direction | 8 | 8 |
| A1 | T1 | Geometric heliostat shading | 4 | 12 |
| A2 | T2 | Current receiver state | 8 | 20 |
| A3 | T3 | Causal historical statistics | 81 | 101 |
| A4 | T4 | Panel-level or lag-derived variables | 5 | 106 |

The 81 A3 candidates comprise nine base variables with nine historical operators each. `window_definition` gives the actual window: `recent4_mean` and `recent8_mean` use 4 s and 8 s despite the legacy `trailing20s` name suffix.

## Dictionary fields and missingness

`feature_id` and `feature_name` retain their frozen values. Units, formulas, source locations, and group assignments retain their prior definitions.

- `raw_missing_rule`: documented upstream construction before model imputation. Rules absent from public notes are explicitly marked unspecified.
- `imputation_rule`: training-partition preprocessing for the relevant input type.
- `missing_handling`: compatibility pointer to these two fields.

The documented first-frame convention for `shadow_ratio_dt`, `newly_shaded_ratio`, and `newly_recovered_ratio` is zero. Panel flux rates are undefined at the first frame. The public notes explicitly document first-frame missingness for the recovery/drop panel IDs, but do not separately specify it for `frame_peak_abs_panel_id`; this revision does not infer that behavior. Historical statistics omit nonfinite observations; no finite observation gives NaN, and a trend needs at least two finite observations at distinct times. Missingness is distinct from an observed zero.

Tabular imputation/encoding and sequence channel median/mean/std are fitted on the training partition only. This does not imply that upstream static cloud-class cutoffs were development-only; see the provenance disclosure below.

## Sequence representation and recorded fold inputs

The separate sequence representation has **11 timepoints × 25 channels**: 12 standardized values, 12 corresponding missing indicators, and one observed-time mask. These channels are not added to the 106 tabular candidates. The sequence models also have a static branch.

`sequence_channel_dictionary_25.csv` supplies zero-based channel indices, documentation labels, roles, base-feature names, groups, and units. Labels ending in `__missing` and `observed_time_mask` are documentation labels, not claims about upstream Python variable names. Values are standardized; `base_unit` records the physical unit before standardization.

`selected_features_by_model_fold.csv` records **repeat 0, outer folds 0–4**, for **E1/M6 (LSTM), E2/M5, and E3/M1-v2**. It is not a complete all-model selection log and does not describe the final development-cohort refit. `input_branch=static` denotes the tabular/static input branch; it does not mean every feature in that branch is time-invariant. For `sequence_value`, `channel_index` preserves the original index and `feature_name` supplies the base variable name. Missing indicators and the time mask are specified in the channel dictionary, not as separately selected rows in this fold table.

## Files

- `feature_dictionary_p24_106.csv`: all 106 candidate definitions, units, tiers, timing, missingness, and source traces.
- `feature_group_mapping_p24.csv`, `excluded_features.csv`: semantic mapping and the sole excluded former candidate, `normalized_sequence_time`.
- `feature_formulas.md`: calculation and preprocessing conventions.
- `sequence_input_11x25.md`, `sequence_channel_dictionary_25.csv`: temporal alignment and all 25 channels.
- `selected_features_by_model_fold.csv`, `feature_source_trace_public.csv`: scoped fold inputs and public source references.
- `schema_and_version.json`, `validation/`: version, frozen-registry reference hash, dictionary hash, and package checks.
- `CHANGELOG.md`, `CITATION.md`, `RIGHTS.md`: revision history, citation guidance, and reuse status.

## Verification scope

From this directory, run:

```sh
python validation/validate_feature_dictionary.py
```

The checker validates package structure, cross-file mappings, tier counts, channel definitions, recorded fold scope, formula references, and the dictionary byte hash. It writes `validation/validation_result.json`. The root `.gitattributes` fixes this dictionary's checkout line endings to LF so its byte hash is portable. The checker does not independently reproduce upstream calculations, compare the private frozen registry, or verify model fitting. Inherited `VERIFIED` evidence statuses refer to the previous source audit; this revision does not perform a new upstream audit. No row-level data, event labels, predictions, fitted weights, or upstream source code are included.

## Link for manuscript use

Reference the feature dictionary directly through its [GitHub documentation link](https://github.com/yudonwansui-cmyk/cloud-prediction/tree/main/prediction/feature_documentation_p24).

Suggested manuscript wording:

> The candidate feature dictionary and input specifications are available at [GitHub](https://github.com/yudonwansui-cmyk/cloud-prediction/tree/main/prediction/feature_documentation_p24).

The link currently serves the public repository version. After this revision is merged into the default branch, the same path will serve the updated documentation. See [CITATION.md](CITATION.md) for link guidance and the source baseline.

## Upstream classification provenance

The area and edge-complexity class cutoffs were calculated from static masks of all **1013** clouds before the 810/203 split. The descriptive evaluation cohort's covariates therefore participated in this pre-existing taxonomy, although no 203-cohort event labels or predictions were used in the earlier documentation audit. This limits a strict development-only preprocessing claim. Exact cutoffs and formulas are in `feature_formulas.md`. The original 200-pixel CLI argument was not archived; the prior audit reports that stored component counts reproduce at the source default of 200 pixels.

## 中文说明

本包为“云影预测：候选特征字典与输入规范”，P24 为冻结预测协议的内部标识。当前版本是 1.1.0 修订草稿，待审阅合并后更新默认分支。

统一使用“开发队列（810 朵云）”“描述性评估队列（203 朵云）”“全部云样本队列（1013 朵云）”。203 朵云曾用于早期研究，不能称为全新未接触的独立测试集。云面积及边界复杂度类别阈值由划分前的全部 1013 朵云静态掩码计算，包含 203 朵云的协变量；不能声称所有上游预处理都仅在开发队列内拟合。

106 项为筛选及类别编码前的候选变量数。A0–A4 为来源层级，T0–T4 为累计输入层级，G1–G7 为物理语义组。时序输入另列为 11×25 张量，不与 106 相加。每折记录仅覆盖 E1/M6、E2/M5、E3/M1-v2 的 repeat 0 外折，并非全部模型或最终重拟合记录。

本次仅整理已有公开证据、字段和名称，不改变特征计算、原始特征名、特征编号、分组、模型选择或既有权利声明。校验通过表示文档包内部一致，不等于重新验证上游源代码及研究结果。
