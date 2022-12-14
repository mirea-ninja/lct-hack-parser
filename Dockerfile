FROM tiangolo/uvicorn-gunicorn-fastapi:latest

WORKDIR /app/

RUN apt-get update && apt-get install -y libgl1-mesa-dev

RUN apt-get install -y libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1

ENV POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.2.0 \
    POETRY_VIRTUALENVS_CREATE=false

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="$PATH:$POETRY_HOME/bin"

# Copy poetry.lock* in case it doesn't exist in the repo
COPY pyproject.toml poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY . /app

CMD ["bash", "./entrypoint.sh"]