FROM python:3.9-bullseye as pybase

WORKDIR /app

ARG LANDSCAPE \
    UID=1000 \
    GID=1000

RUN groupadd -g "${GID}" -r xoxo \
  && useradd -d '/app' -g xoxo -l -r -u "${UID}" xoxo \
  && chown xoxo:xoxo -R '/app'


RUN pip install poetry

COPY ../poetry.lock ../pyproject.toml ./

RUN poetry config virtualenvs.create false \
  && poetry install $(test "$LANDSCAPE" == production && echo "--no-dev") --no-interaction --no-ansi

COPY --chown=xoxo:xoxo ./docker/entrypoint.sh .
COPY --chown=xoxo:xoxo ./xoxo ./xoxo

ENV PYTHONPATH /app
RUN chmod +x './entrypoint.sh'

USER xoxo

ENTRYPOINT ./entrypoint.sh

