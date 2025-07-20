#! /bin/bash
#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"

source .venv/bin/activate

uv sync

uv run prisma db push --schema=prisma

uv run prisma generate --schema=prisma

uv run uvicorn src.main:app --reload --port 8000 --host 0.0.0.0