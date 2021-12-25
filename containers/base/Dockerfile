FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Don't use pip since installs with virutalenvs.create == false will remove
# needed packages
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    POETRY_VERSION=1.1.4 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
ENV PATH="$POETRY_HOME/bin:$PATH"


RUN mkdir -p /workspace
WORKDIR /workspace
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev


# FIXME Change to python module
COPY src ./src
RUN poetry install --no-dev


RUN groupadd -r scriptrunner && \
   useradd --no-log-init -mr -g scriptrunner scriptrunner && \
   chown scriptrunner:scriptrunner -R /workspace
USER scriptrunner
