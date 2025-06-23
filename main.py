import asyncio
import websockets
import json
import re
import dns.resolver
import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# CONFIG
URL = "ws://localhost:8080/domains-only"
KEYWORDS = ["telegram", "teleg", "-tg", "telep"]

# UTILS
def resolves(domain):
    """Check if the domain resolves to an A record."""
    try:
        result = dns.resolver.resolve(domain, 'A')
        return [str(rdata) for rdata in result]
    except:
        return []


def take_screenshot(domain):
    """Take a screenshot of the given domain (skip .dev)."""
    if domain.endswith(".dev") or "*" in domain:
        print(f"[-] Domaine ignoré (wildcard ou .dev): {domain}")
        return None

    url = f"http://{domain}"
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium-browser"

    service = Service("/usr/bin/chromedriver")  # Chemin du chromedriver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.set_page_load_timeout(10)
        driver.get(url)
        os.makedirs("screenshots", exist_ok=True)
        filename = f"screenshots/{domain.replace('.', '_')}.png"
        driver.save_screenshot(filename)
        print(f"[+] Screenshot saved: {filename}")
        return filename
    except Exception as e:
        print(f"[-] Screenshot failed for {domain}: {e}")
        return None
    finally:
        driver.quit()


def save_result(domain, ips, screenshot_file):
    """Save the result to results.csv."""
    file_exists = os.path.isfile("results.csv")
    with open("results.csv", "a", newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Domain", "Resolved IP(s)", "Screenshot"])
        writer.writerow([domain, ", ".join(ips), screenshot_file or "None"])
    print(f"[SAVED] {domain}")

# MAIN LOOP
async def listen():
    """Connect and listen to WebSocket stream, restart on disconnect."""
    while True:
        try:
            async with websockets.connect(URL) as ws:
                async for message in ws:
                    data = json.loads(message)

                    for domain in data.get("data", []):  # domains-only stream
                        if "*" in domain or domain.endswith(".dev"):
                            print(f"[-] Domaine ignoré (wildcard/.dev): {domain}")
                            continue
                        if any(re.search(keyword, domain, re.IGNORECASE) for keyword in KEYWORDS):
                            print(f"[FOUND] {domain}")

                            # Résolution
                            ips = resolves(domain)

                            # Screenshot
                            screenshot_file = take_screenshot(domain)

                            # Sauvegarde
                            save_result(domain, ips, screenshot_file)

        except websockets.exceptions.ConnectionClosedError as e:
            print(f"[!] WebSocket fermé ({e}), reconnexion dans 5s...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"[ERR] {e}, attente 5s...")
            await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(listen())
