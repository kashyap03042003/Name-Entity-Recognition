"""Command-line interface for named entity recognition."""

import argparse
import json
from typing import Sequence

from ner_service.recognizer import DEFAULT_MODEL, EntityRecognizer, get_recognizer


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Extract named entities from a piece of English text."
    )
    parser.add_argument("text", help="Text to analyze")
    parser.add_argument(
        "--model",
        default=None,
        help=f"Installed spaCy model name or path (default: NER_MODEL or {DEFAULT_MODEL})",
    )
    args = parser.parse_args(argv)

    recognizer = EntityRecognizer.load(args.model) if args.model else get_recognizer()
    result = recognizer.predict(args.text)
    print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
