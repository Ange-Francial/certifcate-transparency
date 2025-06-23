from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

def take_screenshot(domain):
    url = f"http://{domain}"
    options = Options()
    options.headless = True
    options.binary_location = "/usr/bin/chromium-browser"  # <-- AJOUTE ÇA SI CHROME NON DISPO
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service("/usr/bin/chromedriver")  # Assure-toi que le chemin est correct
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.set_page_load_timeout(10)
        driver.get(url)
        os.makedirs("screenshots", exist_ok=True)
        filename = f"screenshots/{domain.replace('.', '_')}.png"
        driver.save_screenshot(filename)
        print(f"[+] Screenshot saved: {filename}")
    except Exception as e:
        print(f"[-] Screenshot failed for {domain}: {e}")
    finally:
        driver.quit()

# Test
if __name__ == '__main__':
    take_screenshot("telegwzvx.fit")
