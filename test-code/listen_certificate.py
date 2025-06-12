import certstream

def print_domains(message, context):
    if message['message_type'] != "certificate_update":
        return

    all_domains = message['data']['leaf_cert'].get('all_domains', [])
    if all_domains:
        print("Nouveau certificat émis pour les domaines :")
        for domain in all_domains:
            print(f" - {domain}")

print("[*] Connexion à CertStream...")
certstream.listen_for_events(print_domains, url='wss://certstream.calidog.io/')
