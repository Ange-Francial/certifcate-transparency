# Phishing Detector — CT Log Analysis Tool

## Description

Ce script détecte en temps réel des domaines de phishing potentiels en analysant les logs de certificats SSL via Certificate Transparency (CT), à l’aide de CertStream.

## Dépendances

- Ubuntu
- Python 3
- Firefox + Geckodriver

### Installation :

```bash
sudo apt update
sudo apt install firefox wget tar
wget https://github.com/mozilla/geckodriver/releases/latest/download/geckodriver-linux64.tar.gz
tar -xvzf geckodriver-linux64.tar.gz
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/

pip install -r requirements.txt
