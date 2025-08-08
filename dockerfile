FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS uv

WORKDIR /app

COPY pyproject.toml /app/
COPY README.md /app/
COPY uv.lock /app/

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=README.md,target=README.md \
    uv sync --frozen --no-dev --no-editable

ADD ./src/anki_flashcard_mcp /app/anki_flashcard_mcp

FROM python:3.12-slim-bookworm

WORKDIR /app

COPY --from=uv /app/.venv /app/.venv
COPY --from=uv /app /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

# ENTRYPOINT ["anki-flashcard-mcp"]
CMD ["python3", "-m", "anki_flashcard_mcp.server"]
