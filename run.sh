#! /bin/bash
poetry env activate

poetry install

poetry run uvicorn src.main:app --reload --port 8000 --host 0.0.0.0