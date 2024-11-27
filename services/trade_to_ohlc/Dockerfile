# The builder image, used to build the virtual environment
FROM python:3.11-buster AS builder

# install poetry inside the container
RUN pip install poetry==1.8.4

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# copy the project.toml and poetry.lock files into the container
COPY pyproject.toml poetry.lock /app/

# install python dependencies from the pyproject.toml file
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11.9-slim AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# copy all the source code into the container
COPY . /app

CMD ["python", "-m", "src.main"]