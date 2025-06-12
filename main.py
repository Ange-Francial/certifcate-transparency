import certstream
import Levenshtein
import dns.resolver
import whois
import csv
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# === Configurations ===

keywords = {
    "login": 25, "signin": 25, "account": 25, "verify": 25,
    "paypal": 60, "appleid": 70, "bankofamerica": 60,
    "outlook": 60, "microsoft": 60, "netflix": 60,
    "amazon": 60, "webmail": 50, "secure": 30
}

suspicious_tlds = [".xyz", ".top", ".click", ".buzz", ".icu", ".fit", ".baby", ".online", ".skin"]
score_threshold = 70


# === Fonctions ===

def score_domain(domain):
    score = 0
    domain = domain.lower()
    parts = domain.replace('.', '-').split('-')
    for part in parts:
        for keyword, val in keywords.items():
            if keyword in part or (len(part) >= 6 and Levenshtein.distance(part, keyword) <= 1):
                score += val
    for tld in suspicious_tlds:
        if domain.endswith(tld):
            score += 30
    return score


def resolves(domain):
    try:
        result = dns.resolver.resolve(domain, 'A')
        return len(result) > 0
    except:
        return False


def take_screenshot(domain):
    url = f"http://{domain}"
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
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


def get_registrar(domain):
    try:
        info = whois.whois(domain)
        return info.registrar if info else "Unknown"
    except:
        return "Unknown"


def save_result(domain, screenshot, registrar):
    file_exists = os.path.isfile("results.csv")
    with open("results.csv", "a", newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Domain", "Screenshot", "Registrar"])
        writer.writerow([domain, screenshot, registrar])


def process_domain(domain):
    if not resolves(domain):
        return
    screenshot = take_screenshot(domain)
    registrar = get_registrar(domain)
    save_result(domain, screenshot, registrar)


# === CertStream Listener ===

def certstream_callback(message, context):
    if message['message_type'] != "certificate_update":
        return
    domains = message['data']['leaf_cert']['all_domains']
    for domain in domains:
        if score_domain(domain) >= score_threshold:
            print(f"[!] Suspicious domain: {domain}")
            process_domain(domain)


# === Main Execution ===

if __name__ == "__main__":
    print("[*] Starting phishing detector...")
    certstream.listen_for_events(certstream_callback, url='wss://certstream.calidog.io/')