FROM python:3.11.2

# Set the working directory in the container
WORKDIR /app

# Copy the entire project into the working directory
COPY . /app

# Install Poetry (latest version)
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Install dependencies from the pyproject.toml using Poetry
RUN poetry install

# Run the app using Poetry
CMD ["poetry", "run", "python", "app.py"]
