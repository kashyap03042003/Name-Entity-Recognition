# Named Entity Recognition

A small, ready-to-run Named Entity Recognition (NER) service for extracting
people, organizations, places, dates, and other entities from English text.
It uses spaCy's pretrained English pipeline and exposes the same predictions
through both an HTTP API and a command-line interface.

> This is a general-purpose demonstration, not a domain-specific or
> human-reviewed information extraction system. Validate results before using
> them for consequential decisions.

## Features

- Extract named entities and return their text, label, and character offsets.
- Predict through a JSON API built with FastAPI.
- Process text from the command line and print JSON results.
- Configure the spaCy model with an environment variable.
- Validate input length and reject blank requests.
- Run the API in a container or locally.

## How it works

The application loads a spaCy English NER pipeline (by default
`en_core_web_sm`). The model detects entity spans in the supplied text. Each
prediction includes the entity string, spaCy label, and start/end character
offsets in the original input. Offsets use Python's zero-based, end-exclusive
convention.

This repository uses a pretrained model; it does not train or fine-tune a
model on a project-specific dataset. The small model is intended for a quick
demonstration and may miss entities, assign imperfect labels, or perform poorly
on specialized text.

## Requirements

- Python 3.10 or newer
- pip
- Internet access for installing the spaCy English model

## Install

Clone the repository and install the package:

```bash
git clone https://github.com/kashyap03042003/Name-Entity-Recognition.git
cd Name-Entity-Recognition
python -m venv .venv
```

Activate the environment, then install the project and test dependencies:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -e ".[test]"
python -m spacy download en_core_web_sm
```

## Use the command line

Pass the text to `ner-predict`:

```bash
ner-predict "Apple hired John Smith in New York on Monday."
```

The command prints JSON in this format:

```json
{
  "text": "Apple hired John Smith in New York on Monday.",
  "entities": [
    {
      "text": "Apple",
      "label": "ORG",
      "start": 0,
      "end": 5
    },
    {
      "text": "John Smith",
      "label": "PERSON",
      "start": 12,
      "end": 22
    },
    {
      "text": "New York",
      "label": "GPE",
      "start": 26,
      "end": 34
    },
    {
      "text": "Monday",
      "label": "DATE",
      "start": 38,
      "end": 44
    }
  ]
}
```

Entity predictions can differ by model version and input, so treat this output
as an illustration rather than a guaranteed result. To use a different
installed spaCy pipeline, set `NER_MODEL` to its package name:

```bash
NER_MODEL=en_core_web_md ner-predict "Text to analyze."
```

## Run the HTTP API

Start the local development server:

```bash
uvicorn ner_service.api:app --reload
```

Interactive API documentation is available at
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### `POST /predict`

Request:

```json
{
  "text": "Ada Lovelace worked with Charles Babbage in London."
}
```

Example response:

```json
{
  "text": "Ada Lovelace worked with Charles Babbage in London.",
  "entities": [
    {
      "text": "Ada Lovelace",
      "label": "PERSON",
      "start": 0,
      "end": 12
    },
    {
      "text": "Charles Babbage",
      "label": "PERSON",
      "start": 25,
      "end": 40
    },
    {
      "text": "London",
      "label": "GPE",
      "start": 44,
      "end": 50
    }
  ]
}
```

The API accepts non-empty text up to 5,000 characters. Invalid requests return
HTTP 422 with validation details. A lightweight `GET /health` endpoint returns
the process health status.

Example using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"Ada Lovelace worked with Charles Babbage in London."}'
```

Set `NER_MODEL` to the name of another installed spaCy pipeline to select a
different model:

```bash
NER_MODEL=en_core_web_md uvicorn ner_service.api:app
```

## Run with Docker

Build the image and start the service:

```bash
docker build -t ner-service .
docker run --rm -p 8000:8000 ner-service
```

The image installs the default English model during its build.

## Development and tests

Run the automated tests with:

```bash
pytest
```

Tests use a deterministic fake recognizer, so they do not need to download the
spaCy language model.

## Project structure

```text
src/ner_service/
  api.py          FastAPI application and prediction endpoint
  cli.py          Command-line prediction tool
  recognizer.py   spaCy model loading and entity extraction
  schemas.py      Validated API request and response models
tests/            API, validation, and recognizer tests
Dockerfile        Container image for the API
pyproject.toml    Package metadata and dependencies
LICENSE           MIT license
```

## License

This project is licensed under the [MIT License](LICENSE).
