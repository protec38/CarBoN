FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install

ENV STATIC_ROOT /static
CMD ["/app/entrypoint.sh"]