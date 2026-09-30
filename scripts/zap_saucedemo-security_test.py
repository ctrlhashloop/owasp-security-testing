import time
import os
import subprocess
from zapv2 import ZAPv2

# Configuration (defaults to local docker/daemon ports)
ZAP_API_KEY = ""  # Disabled by default in headless test runs
ZAP_PROXY = "http://127.0.0.1:8080"
TARGET_URL = "https://www.saucedemo.com/"


def start_zap_daemon():
    """Starts ZAP in headless daemon mode if not already running."""
    print("Launching OWASP ZAP in background daemon mode...")
    # This command starts ZAP headlessly on port 8080 with API key disabled for easy access
    zap_process = subprocess.Popen(
        ["zap.sh", "-daemon", "-host", "127.0.0.1", "-port", "8080", "-config", "api.disablekey=true"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Wait a few seconds for ZAP daemon to initialize
    print("Waiting for ZAP daemon to boot up...")
    time.sleep(15)
    return zap_process


def run_local_security_test():
    # If running inside CI/Docker container, you can optionally launch ZAP programmatically:
    # zap_process = start_zap_daemon()

    print(f"Connecting to ZAP instance at {ZAP_PROXY}...")

    zap = ZAPv2(
        apikey=ZAP_API_KEY,
        proxies={'http': ZAP_PROXY, 'https': ZAP_PROXY}
    )

    # 1. Prime target URL
    print(f"Accessing target: {TARGET_URL}")
    try:
        zap.urlopen(TARGET_URL)
    except Exception as e:
        print(f"Warning/Connection note: {e}")
    time.sleep(2)

    # 2. Run Spider Scan
    print("Starting Spider crawl...")
    scan_id = zap.spider.scan(TARGET_URL)

    while int(zap.spider.status(scan_id)) < 100:
        print(f"Spider progress: {zap.spider.status(scan_id)}%")
        time.sleep(2)
    print("Spider scan completed.")

    # 3. Wait for Passive Scan queue to clear
    print("Waiting for passive vulnerability checks to finish processing...")
    while int(zap.pscan.records_to_scan) > 0:
        print(f"Records pending passive scan: {zap.pscan.records_to_scan}")
        time.sleep(2)
    print("Passive scan completed.")

    # 4. Generate HTML Report
    reports_dir = os.path.abspath("reports")
    os.makedirs(reports_dir, exist_ok=True)
    report_file = "zap_scan_report.html"

    print("Generating HTML report...")
    try:
        html_report = zap.core.htmlreport()
        report_path = os.path.join(reports_dir, report_file)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_report)
        print(f"Report successfully saved to: {report_path}")
    except Exception as e:
        print(f"Error generating HTML report via API: {e}")

    # 5. Summary
    alerts = zap.core.alerts(baseurl=TARGET_URL)
    print(f"\nScan finished! Total findings: {len(alerts)}")
    for alert in alerts:
        print(f"[{alert.get('risk')}] {alert.get('alert')} -> {alert.get('url')}")


if __name__ == "__main__":
    run_local_security_test()