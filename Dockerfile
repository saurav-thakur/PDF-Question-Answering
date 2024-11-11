FROM python:3.11.2 as builder

WORKDIR /app

COPY . /app

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ENV PATH="/root/.local/bin:$PATH" && \
    poetry install --no-root && \
    rm -rf /root/.cache/pypoetry

FROM python:3.11.2

WORKDIR /app

COPY --from=builder /app /app

CMD ["poetry", "run", "python", "app.py"]
