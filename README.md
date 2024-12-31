# MCQ Generator Using spaCy

This repository contains a Python script for generating multiple-choice questions (MCQs) from a given text. The script leverages spaCy for natural language processing to extract nouns and create meaningful questions.

## Features

- Extracts sentences from input text to generate questions.
- Selects nouns as the basis for creating question blanks and options.
- Provides distractors for the generated MCQs for better challenge.

## Requirements

The following Python libraries are required to run the script:

- `spacy`
- `random`
- `collections.Counter`

1. Install the dependencies using pip:
   ```bash
   pip install spacy

2. Install spaCy and the required model:
  ```bash
   pip install spacy
  python -m spacy download en_core_web_sm

