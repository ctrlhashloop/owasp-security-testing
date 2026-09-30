import time
import os
from zapv2 import ZAPv2

# Configuration
ZAP_API_KEY = "your_zap_api_key_here"  # Match your ZAP settings, or leave "" if disabled
ZAP_PROXY = "http://127.0.0.1:8080"
TARGET_URL = "https://www.saucedemo.com/"


def run_local_security_test():
    print(f"Connecting to local ZAP instance at {ZAP_PROXY}...")

    zap = ZAPv2(
        apikey=ZAP_API_KEY,
        proxies={'http': ZAP_PROXY, 'https': ZAP_PROXY}
    )

    # 1. Prime target URL
    print(f"Accessing target: {TARGET_URL}")
    zap.urlopen(TARGET_URL)
    time.sleep(2)

    # 2. Run Spider Scan to map out application nodes
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

    print(f"Generating HTML report...")
    try:
        # Using the core html report method
        html_report = zap.core.htmlreport()
        report_path = os.path.join(reports_dir, report_file)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_report)
        print(f"Report successfully saved to: {report_path}")
    except Exception as e:
        print(f"Error generating HTML report via API: {e}")

    # 5. Print out a quick console summary
    alerts = zap.core.alerts(baseurl=TARGET_URL)
    print(f"\nScan finished! Total findings: {len(alerts)}")
    for alert in alerts:
        print(f"[{alert.get('risk')}] {alert.get('alert')} -> {alert.get('url')}")


if __name__ == "__main__":
    run_local_security_test()