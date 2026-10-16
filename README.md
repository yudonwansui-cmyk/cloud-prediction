# Cloud-shadow prediction: candidate feature dictionary and input specification

**Version 1.1.0.**

Definitions for the **106 candidate tabular predictors**, feature tiers, missingness rules, and the separate **11 × 25 sequence input** are in [prediction/feature_documentation_p24/](prediction/feature_documentation_p24/). P24 identifies the frozen prediction protocol.

The study comprises a **development cohort (810 clouds)** and a **descriptive evaluation cohort (203 clouds)**, together the **full cloud cohort (1013 clouds)**. The 203-cloud cohort had been used in earlier research and is not an untouched independent test. Static cloud-class cutoffs were calculated using all 1013 masks before the split.

This English-only package contains CSV, Markdown, JSON, and a consistency checker. It contains no row-level research data, event labels, predictions, fitted weights, or implementation code. The revision changes documentation, not feature calculations or model results.

The feature dictionary can be cited directly using its [documentation link](https://github.com/yudonwansui-cmyk/cloud-prediction/tree/main/prediction/feature_documentation_p24). See [CHANGELOG.md](prediction/feature_documentation_p24/CHANGELOG.md) for revision details.

**Rights:** All rights reserved. See [RIGHTS.md](prediction/feature_documentation_p24/RIGHTS.md) and [CITATION.md](prediction/feature_documentation_p24/CITATION.md).
