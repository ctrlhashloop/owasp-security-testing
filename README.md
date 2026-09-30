# OWASP ZAP Python Security Testing Pipeline

This repository demonstrates an automated DevSecOps security-testing pipeline that integrates **OWASP ZAP (Zed Attack Proxy)** and **Python** via **GitHub Actions** to perform continuous baseline vulnerability assessments against a target web application ([Swag Labs](https://www.saucedemo.com/)).

---

## 🚀 Key Features
* **Automated CI/CD Execution:** Runs scheduled weekly scans and triggers automatically on every pull request or push to the `main` branch.
* **Headless Daemon Integration:** Spins up OWASP ZAP securely inside ephemeral Linux container runners.
* **Python Automation Wrapper (`zaproxy`):** Drives application spider crawling, passive scan queue monitoring, and programmatic report generation.
* **Artifact Archiving:** Automatically compiles and stores comprehensive HTML security audit reports as downloadable workflow artifacts for compliance tracking.

---

## 🛠️ Tech Stack & Tools
* **Security Tool:** OWASP ZAP (Daemon Mode)
* **Automation:** Python (`zaproxy` API client)
* **CI/CD Platform:** GitHub Actions (Ubuntu Runners)
* **Containerization:** Docker
* **Target Application:** Swag Labs (E-commerce Vulnerability Testbed)

---

## ⚙️ How the Pipeline Works
1. **Environment Provisioning:** The GitHub Actions runner initializes and boots up an isolated OWASP ZAP background daemon container with permissive local API access rules.
2. **Target Discovery (Spidering):** A custom Python script connects to the local ZAP API, priming the target URL (`https://www.saucedemo.com/`) and executing an automated spider crawl to map application endpoints.
3. **Passive Vulnerability Analysis:** The script monitors background analysis queues until all incoming traffic has been passively analyzed for standard security misconfigurations (e.g., missing security headers, weak cookie flags).
4. **Report Generation:** ZAP compiles the findings into an interactive HTML security report, which is exported and archived for audit readiness.

---

## 📂 Repository Architecture
```text
pci-zap-security-test/
├── .github/
│   └── workflows/
│       └── zap-ci.yml            # CI/CD pipeline automation workflow
├── reports/                      # Auto-generated HTML audit reports
├── requirements.txt              # Python project dependencies
├── zap_local_test.py             # Python script driving the ZAP API logic
└── README.md                     # Project documentation
```

---

## 💻 Running Locally

### 1. Prerequisites
* Python 3.11+
* Docker installed and running

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start ZAP Daemon via Docker
Spin up OWASP ZAP locally in background daemon mode with API permissions enabled:
```bash
docker run -d \
  --name zap-daemon \
  -p 8080:8080 \
  ghcr.io/zaproxy/zaproxy:stable \
  zap.sh -daemon \
  -host 0.0.0.0 \
  -port 8080 \
  -config api.disablekey=true \
  -config api.addrs.addr.name=.* \
  -config api.addrs.addr.regex=true
```

### 4. Execute the Security Script
Run your custom Python automation script to drive the scan and generate the report:
```bash
python zap_local_test.py
```
Your compiled HTML security report will be saved inside the `reports/` directory.

---

## ⚙️ CI/CD Pipeline Workflow (`zap-ci.yml`)

```yaml
name: ZAP Python Security Pipeline

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
  schedule:
    - cron: '0 2 * * 1' # Every Monday at 2 AM

jobs:
  security_scan:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Start OWASP ZAP Daemon Container
        run: |
          docker run -d \
            --name zap-daemon \
            -p 8080:8080 \
            ghcr.io/zaproxy/zaproxy:stable \
            zap.sh -daemon \
            -host 0.0.0.0 \
            -port 8080 \
            -config api.disablekey=true \
            -config api.addrs.addr.name=.* \
            -config api.addrs.addr.regex=true

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Wait for ZAP to Initialize
        run: |
          echo "Waiting for ZAP API to become ready..."
          until curl -s http://localhost:8080/JSON/core/view/version/; do
            sleep 3
          done
          echo "ZAP is up and running!"

      - name: Run Security Automation Script
        run: python zap_local_test.py

      - name: Upload Security Report Artifact
        uses: actions/upload-artifact@v4
        with:
          name: zap-html-security-report
          path: reports/zap_scan_report.html
```

---

## 🛡️ Compliance & Security Context
This project mirrors enterprise **Vulnerability Management** practices required by security frameworks (such as **PCI DSS v4.0.1** software testing and automated vulnerability scanning guidelines), ensuring web application risks are identified early in the software development lifecycle (SDLC).