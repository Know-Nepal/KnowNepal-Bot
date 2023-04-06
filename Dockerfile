FROM python:3.10-slim-buster

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN pip install poetry

COPY . /code

RUN poetry config virtualenvs.create false\
    && poetry install --no-dev --no-interaction --no-ansi

RUN chmod +x entrypoint.sh
CMD [ "python server.py" ]
EXPOSE 3000
ENTRYPOINT [ "sh", "entrypoint.sh" ]