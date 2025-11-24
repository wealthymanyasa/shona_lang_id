---
license: cc-by-4.0
language: ["en", "sn"]
multilinguality: multilingual
size_categories: 100K<n<1M
task_categories: ["text-classification"]
task_ids: ["language-identification"]
---

# English–Shona Language ID Dataset

A comprehensive dataset for language identification tasks containing English and Shona sentences, formatted for FastText training.

## Overview

This dataset contains **763,546** labeled sentences in English and Shona languages, designed for training and evaluating language identification models. The data is cleaned, balanced, and formatted specifically for FastText-style supervised learning.

## Dataset Structure

```
data/
├── shona_en_lang_train.txt    # Training set (135 MB)
├── shona_en_lang_valid.txt    # Validation set (16.9 MB)
└── shona_en_lang_test.txt     # Test set (16.9 MB)
```

## Data Format

Each line in the dataset files follows the FastText format:
```
__label__en [English sentence]
__label__shona [Shona sentence]
```

**Example:**
```
__label__en It was about three o 'clock before we could take a break .
__label__shona Ndakapindura kuti , " Hungu , Munyengetero waShe . "
```

## Dataset Statistics

- **Total sentences:** 763,546
- **Languages:** English (en), Shona (shona)
- **Training set:** ~600,000 sentences
- **Validation set:** ~80,000 sentences
- **Test set:** ~80,000 sentences
- **License:** CC BY 4.0

## Usage

### For FastText Training

```python
import fasttext

# Train a supervised language identification model
model = fasttext.train_supervised(
    input="data/shona_en_lang_train.txt",
    epoch=25,
    lr=1.0,
    wordNgrams=2,
    dim=100,
    loss='softmax'
)

# Test the model
result = model.test("data/shona_en_lang_test.txt")
print(f"Accuracy: {result[1]:.2f}%")

# Predict language of new text
text = "Hello, how are you?"
prediction = model.predict(text)
print(f"Language: {prediction[0][0].replace('__label__', '')}")
```

### For Other ML Frameworks

The dataset can be easily adapted for scikit-learn, PyTorch, TensorFlow, or other machine learning frameworks by parsing the label and text components.

## Publishing to Hugging Face

The repository includes a script for publishing the dataset to Hugging Face Hub:

```python
from huggingface_publisher import publish_dataset

# Publish dataset
publish_dataset(
    hf_token="your_hf_token",
    repo_id="your-username/english-shona-langid",
    dataset_files=[
        "data/shona_en_lang_train.txt",
        "data/shona_en_lang_valid.txt", 
        "data/shona_en_lang_test.txt"
    ],
    readme_file="README.md"
)
```

## Dependencies

See `requirements.txt` for the complete list of dependencies. Key packages include:

- `huggingface_hub>=1.1.5` - For dataset publishing
- `fasttext` - For model training (optional)

## License

This dataset is released under the **Creative Commons Attribution 4.0 International License**. You are free to share, adapt, and use the dataset for any purpose, provided you give appropriate credit.

## Citation

If you use this dataset in your research or projects, please cite:

```
English–Shona Language ID Dataset. (2025). 
Available at: https://huggingface.co/datasets/omanyasa/english-shona-langid
```

## Contributing

Contributions to improve the dataset are welcome. Please ensure any additions maintain the quality and format consistency of the existing data.

## Acknowledgments

This dataset was created to support language identification research and applications involving English and Shona languages, particularly for African NLP initiatives.
