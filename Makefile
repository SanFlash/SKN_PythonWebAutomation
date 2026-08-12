# Darshan Hotel — Playwright + Pytest + Allure Automation Framework
# Author: Satyendra Kumar Namdeo
# This authorship notice is part of the project source and must be
# preserved in copies and forks (see NOTICE.md and LICENSE).

.PHONY: install test smoke regression allure-report clean docker-build docker-test

install:
	pip install -r requirements.txt
	playwright install --with-deps

test:
	pytest

smoke:
	pytest -m smoke

regression:
	pytest -m regression

# Requires the Allure commandline tool (https://allurereport.org/docs/install/)
allure-report:
	allure generate allure-results --clean -o allure-report
	allure open allure-report

docker-build:
	docker build -t darshanhotel-playwright-python .

docker-test:
	docker run --rm -v $(PWD)/allure-results:/app/allure-results -v $(PWD)/reports:/app/reports darshanhotel-playwright-python

clean:
	rm -rf allure-results allure-report reports test-results playwright-report .pytest_cache logs
	find . -type d -name "__pycache__" -exec rm -rf {} +
