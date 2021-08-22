FROM python:3.9.6-bullseye

# Install poetry, the dependency manager
RUN POETRY_VERSION=1.1.8 curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /usr/src/app

COPY pyproject.toml ./
COPY poetry.lock ./

RUN poetry install

COPY . .

CMD [ "poetry", "run", "python", "src/app/main.py" ]