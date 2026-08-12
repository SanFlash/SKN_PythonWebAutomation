# Darshan Hotel — Playwright + Pytest + Allure Automation Framework
# Author: Satyendra Kumar Namdeo
# This authorship notice is part of the project source and must be
# preserved in copies and forks (see NOTICE.md and LICENSE).
#
# Official Playwright image — browsers + OS deps already installed,
# so the container is reproducible regardless of the host machine.
FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy

LABEL maintainer="Satyendra Kumar Namdeo"
LABEL org.opencontainers.image.authors="Satyendra Kumar Namdeo"
LABEL org.opencontainers.image.title="Darshan Hotel Playwright Pytest Automation"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV APP_ENV=dev
ENV PYTHONUNBUFFERED=1

CMD ["pytest"]
