# ScamShield AI — ML Models Directory

This directory stores trained machine learning model artifacts for lexical URL classification and social-engineering message detection.

## Artifacts

- `scam_url_model.joblib`: Trained `RandomForestClassifier` pipeline trained on a 26-dimensional combined feature vector (lexical, structural, entropy, and intent markers).
- Model persistence via `joblib`.

## Training & Reproducibility

To re-train or benchmark the model pipeline:

```bash
python evaluation/evaluate.py
```

This will automatically:
1. Load `evaluation/dataset/urls.csv` and `evaluation/dataset/messages.csv`.
2. Extract the unified 26-feature numerical vector.
3. Perform 5-Fold Stratified Cross Validation.
4. Fit the production pipeline and save `scam_url_model.joblib`.
5. Output verified metrics to `evaluation/results/metrics.json` and plot `confusion_matrix.png`.
