# Readme

Guide to all the files:

- **Folder Intent Extraction**:
  - ```avocado_train_target_sentences.parquet```:
    - train split that contains a column for target sentences that contain some sort of request
  - ```avocado_train.parquet```
    - train split from avocado
- ```intent_clustering_model_extracted_text```
  - Trained BERTopic Model (possibly PICKLE format) on column ```extracted_text```
- ```intent_clustering_model_target_sentence```
  - Trained BERTopic Model (possibly PICKLE format) on column ```target_sentence```
