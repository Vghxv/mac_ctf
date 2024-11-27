# Use an official Python runtime as a parent image
FROM python:3.11-buster

# Set the working directory
WORKDIR /app

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi

# Copy the rest of the code
COPY . /app

EXPOSE 5000

CMD ["python", "main.py"]
