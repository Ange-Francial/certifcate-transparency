Voici un **README.md prêt à l'emploi** reprenant toutes les informations détaillées que nous avons vues :

---

# 🔥 **Phishing Detector via CT Logs**

*Un outil de surveillance en temps réel des Certificate Transparency Logs pour identifier des domaines suspects.*

---

## 🎯 **Objectif du projet**

Ce projet permet de :

* Se **connecter à un serveur de CT Logs** (Certificate Transparency) via WebSocket.
* **Filtrer** les domaines suspects basés sur des mots-clés spécifiques (`telegram`, `teleg`, `tele`).
* Exclure automatiquement les **wildcards (`*.`)** ainsi que les **domaines `.dev`**.
* Faire des **vérifications DNS** (`A record`) des domaines suspects.
* Générer des **captures d’écran** des sites suspects.
* Exporter toutes les informations utiles (`domaine`, `IP(s)`, `capture`) vers un fichier `results.csv`.
* Gérer automatiquement la **reconnexion WebSocket** en cas de coupure.

---

## 🗂️ **Arborescence du Projet**

```
certifcate-transparency/
├─ main.py                      # Script principal du listener
├─ results.csv                  # Fichier de résultats (domaine, IP, capture d’écran)
├─ screenshots/                # Dossier des captures d’écran
├─ test-code/
│  └─ test_screenshot.py       # Script de test de capture d’écran
├─ certstream-server-go/       # Serveur certstream
├─ requirements.txt            # Dépendances Python
├─ README.md                    # Documentation du projet
```

---

## ⚡️ **Composants du Projet**

### 1️⃣ **certstream-server-go**

✅ Émet un flux de domaines extraits des CT Logs officiels.
▶️ Endpoint utilisé : `ws://localhost:8080/domains-only`

#### Lancement :

```bash
go build -o certstream-server ./cmd/certstream-server-go
cp config.sample.yaml config.yaml
./certstream-server
```

---

### 2️⃣ **main.py**

✅ Consomme le flux WebSocket du serveur certstream.
✅ Analyse en temps réel chaque nom de domaine.
✅ Critères :

* Domaine contenant `telegram|teleg|tele`.
* Exclut : wildcard (`*.`), `.dev`.
  ✅ Actions :
* Résolution IP via DNS.
* Capture d’écran du site.
* Export des résultats (`results.csv`).

---

### 3️⃣ **test\_screenshot.py**

✅ Script isolé pour tester la capture d’écran du site.

---

### 4️⃣ **results.csv**

✅ Export des résultats :

| Domain         | Resolved IP(s)                  | Screenshot                     |
| -------------- | ------------------------------- | ------------------------------ |
| telegfvcg.baby | 104.21.51.231, 172.67.190.161   | screenshots/telegfvcg_baby.png |

---

## ⚡️ **Pré-requis Techniques**

* 🐍 **Python 3.12+**
* 🐳 **Go 1.22+**
* 🌐 **certstream-server-go** compilé
* ⚡️ **Google Chrome / Chromium** + `chromedriver` installé
* ✅ Dépendances Python :

  ```
  websockets
  dnspython
  selenium
  ```

---

## 🚀 **Installation & Exécution**

### 1️⃣ Lancement du serveur `certstream-server-go`

```bash
cd certstream-server-go/
go build -o certstream-server ./cmd/certstream-server-go
cp config.sample.yaml config.yaml
./certstream-server
```

### 2️⃣ Installation des dépendances Python

```bash
pip install -r requirements.txt
```

### 3️⃣ Exécution du listener

```bash
python3 main.py
```

---

## ⚡️ **Exemple de Logs**

```
[FOUND] ww25.xwwh.yd10-telegram.org
[+] Screenshot saved: screenshots/ww25_xwwh_yd10-telegram_org.png
[SAVED] ww25.xwwh.yd10-telegram.org
[-] Domaine ignoré (wildcard/.dev): *.lordserialru21.biz
[-] Domaine ignoré (wildcard/.dev): *.frc-stage.com

```

---

## ⚡️ **Gestion des erreurs intégrée**

✅ Wildcards (`*.`) ➔ Ignorés automatiquement
✅ Domaines `.dev` ➔ Ignorés automatiquement
✅ Déconnexion du WebSocket ➔ Reconnexion après 5s
✅ Timeouts de capture d’écran ➔ Gérés avec `try/except`
✅ Échec de résolution DNS ➔ Domaine sauté

---