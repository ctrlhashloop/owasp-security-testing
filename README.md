# OWASP ZAP Security Testing Pipeline

This repository demonstrates a lightweight security-testing project integrating **OWASP ZAP (Zed Attack Proxy)** via **GitHub Actions** to perform automated baseline vulnerability scans against a web application target ([Swag Labs](https://www.saucedemo.com/)).

## Overview
* **Target Application:** Swag Labs (Demo E-commerce App)
* **Testing Tool:** OWASP ZAP Baseline Scan Container
* **Automation Platform:** GitHub Actions

## Running Locally via Docker
You can execute the same baseline scan locally using Docker without installing full client tools:

```bash
docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
    -t [https://www.saucedemo.com/](https://www.saucedemo.com/) \
    -r reports/zap_report.html