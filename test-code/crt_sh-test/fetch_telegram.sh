#!/bin/bash

DATE_DEBUT=$(date "+%Y-05-01")
FICHIER_SORTIE="certificats_telegram_$(date '+%Y-05').json"

echo "[*] Récupération des certificats telegram à partir du ${DATE_DEBUT}..."
reponse=$(curl -s "https://crt.sh/?q=telegram&output=json&exclude=expired")

# ✅ Vérification si la réponse est du JSON valide
if ! echo "$reponse" | jq empty 2>/dev/null; then
    echo "[✗] La réponse de crt.sh n'est PAS du JSON valide."
    echo "[ℹ️] Contenu reçu :"
    echo "$reponse"
    exit 1
fi

# ✅ Si valide, filtrage
echo "$reponse" | jq --arg DATE_DEBUT "$DATE_DEBUT" '.[] | select(.not_before >= $DATE_DEBUT)' \
    > "${FICHIER_SORTIE}"

echo "[✓] Résultats enregistrés dans ${FICHIER_SORTIE}"
