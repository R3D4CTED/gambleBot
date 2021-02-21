# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster
LABEL maintainer="https://github.com/R3D4CTED/gambleBot"

ENV BOT_PREFIX="" \
    BOT_TOKEN="" \
    DB_USER="" \
    DB_PASS="" \
    LOG_LEVEL="" \
# Keeps Python from generating .pyc files in the container
    PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
USER appuser

# Running Database initialisation/other scripts
RUN python init.py

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "main.py"]
