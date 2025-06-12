# Phishing Detector — CT Log Analysis Tool

## Description

Ce script détecte en temps réel des domaines de phishing potentiels en analysant les logs de certificats SSL via Certificate Transparency (CT), à l’aide de CertStream.

## Dépendances

- Ubuntu
- Python 3
- Firefox + Geckodriver

## Installation :

### 1. Installer Python et pip
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 2. Créer un environnement virtuel
```bash
python3 -m venv phishing-env
source phishing-env/bin/activate
```

### 3. Installer les dépendances Python
```bash
pip install certstream selenium requests python-Levenshtein dnspython whois
```

### 4. Installer ZDNS (pour la résolution DNS rapide)

#### Installer Go
```bash
sudo apt install golang-go
```

#### Cloner et compiler ZDNS
```bash
git clone https://github.com/zmap/zdns.git
cd zdns
go build
sudo cp zdns /usr/local/bin/
cd ..
```

### 5. Installer Geckodriver (driver pour Selenium + Firefox)
```bash
sudo apt install wget tar
wget https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz
tar -xvzf geckodriver-v0.36.0-linux64.tar.gz 
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/

geckodriver --version
```