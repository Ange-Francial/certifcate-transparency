import certstream

KEYWORDS = ["telegram", "teleg", "tele"]

def callback(message, context):
    if message.get("message_type") != "certificate_update":
        return
    domains = message["data"]["leaf_cert"].get("all_domains", [])

    for domain in domains:
        if any(keyword in domain.lower() for keyword in KEYWORDS):
            print(f"[PHISHING CANDIDAT] {domain}")

print("[*] Connexion à CertStream...")
certstream.listen_for_events(callback, url='wss://certstream.calidog.io/')