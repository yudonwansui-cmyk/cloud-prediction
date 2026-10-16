# Cloud-shadow prediction: candidate feature dictionary and input specification

**Review draft, version 1.1.0.** Based on public commit `f72d446a5c3d985f60c0acad47d31bb1cd0c44d8`; this proposed revision is under review.

Definitions for the **106 authorized candidate tabular predictors**, their source and cumulative tiers, missingness rules, and the separate **11 × 25 sequence input** are in [`prediction/feature_documentation_p24/`](prediction/feature_documentation_p24/). P24 is the internal identifier of the frozen prediction protocol.

The study comprises a **development cohort (810 clouds)** and a **descriptive evaluation cohort (203 clouds)**, together the **full cloud cohort (1013 clouds)**. The 203-cloud cohort had been used in earlier research and is not an untouched independent test. Static cloud-class cutoffs were calculated using all 1013 masks before the split, as disclosed in the package README.

The package contains CSV, Markdown, JSON, and a consistency checker. It contains no row-level research data, event labels, predictions, fitted weights, or upstream code. This revision changes documentation fields and labels, not feature calculations or model results.

The feature dictionary can be cited directly using its [documentation link](https://github.com/yudonwansui-cmyk/cloud-prediction/tree/main/prediction/feature_documentation_p24). See [CHANGELOG.md](prediction/feature_documentation_p24/CHANGELOG.md) for revision details.

**Rights:** All rights reserved. No reuse license is granted; see [`RIGHTS.md`](prediction/feature_documentation_p24/RIGHTS.md). A formal manuscript citation is not yet available; see [`CITATION.md`](prediction/feature_documentation_p24/CITATION.md).
