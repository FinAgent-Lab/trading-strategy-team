#! /bin/bash
#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"

poetry env activate

poetry install

poetry run prisma generate --schema=prisma

poetry run uvicorn src.main:app --reload --port 8000 --host 0.0.0.0