import time
from zapv2 import ZAPv2


# Configurations
ZAP_PROXY = "http://127.0.0.1:8080"
TARGET_URL = "https://www.saucedemo.com/"

def run_local_security_tests():
    print(f"Connecting to local ZAP instance at {ZAP_PROXY}...")

    # Initialize the ZAP client wrapper
    zap = ZAPv2(
        proxies={'http': ZAP_PROXY, 'https': ZAP_PROXY}
    )

    # 1. Prime target URL so ZAP starts tracking it
    print(f"Accessing target: {TARGET_URL}")
    zap.urlopen(TARGET_URL)
    time.sleep(5)

    # 2. Run Spider Scan (Crawling the application structure)
    print("Starting Spider crawl...")
    scan_id = zap.spider.scan(TARGET_URL)

    # Wait for the spider to hit 100% completion
    while int(zap.spider.status(scan_id)) < 100 :
        progress = zap.spider.status(scan_id)
        print(f"Spider progress: {progress}%")
        time.sleep(4)
    print("Spider scan completed successfully.")

    # Brief pause to let passive scan queues finish processing
    time.sleep(3)

    # 3. Pull and display vulnerability alerts
    print("\nFetching security findings...")
    alerts = zap.core.alerts(baseurl=TARGET_URL)

    if not alerts:
        print("No security Alerts found.")
        return
    print(f"Found {len(alerts)} potential findings:\n")
    for alert in alerts:
        risk = alert.get("risk")
        name = alert.get("name")
        url = alert.get("url")
        print(f"Found {risk} and {name}.")
        print(f"   -> Affected URL: {url}\n")

if __name__ == "__main__":
    run_local_security_tests()