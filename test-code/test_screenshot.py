from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import os

def take_screenshot(domain):
    url = f"http://{domain}"
    options = Options()
    options.headless = True

    # Créer un profil vierge
    profile = FirefoxProfile()
    options.profile = profile  # <- nouvelle syntaxe

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

# === TEST ===
domain_test = "google.com"
take_screenshot(domain_test)
