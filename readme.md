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

 **Folder**

```
Project Structure
│
├── 01_avocado_preprocessing
│   ├── 01_parse_avocado_xml.ipynb
│   ├── 02_avocado_confirm_correct.ipynb
│   ├── 03_avocado_extract_text.ipynb
│   └── 04_avocado_split_dataset.ipynb
│
├── 02_intent_extraction
│   ├── 01_heuristics
│   │   └── 01_heuristic.ipynb
│   ├── 02_clustering
│   │   └── ..
│   └── 03_llm_prompting
│       └── ..
│
│
├── data
│   ├── bertopic_models
│   │   └── ...
│   │
│   ├── avocado_full.parquet 
│   ├── avocado_test.parquet
│   ├── avocado_train.parquet
│   └── avocado_val.parquet
│
└── README.md
```
