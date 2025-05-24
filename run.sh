#!/bin/bash

set -e

# Chemin du script Python
SCRIPT="arch_wiki_docs.py"

# Crée un venv s’il n’existe pas
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Active le venv
source venv/bin/activate

# Vérifie si les paquets sont installés
REQUIREMENTS_INSTALLED=$(pip list --format=freeze | grep -c "^requests==")
if [ "$REQUIREMENTS_INSTALLED" -eq 0 ]; then
    echo "Installing requirements..."
    pip install --upgrade pip
    pip install requests
fi

# Lancer le script Python avec tous les arguments passés à run.sh
echo "Running: python3 $SCRIPT $*"
python3 "$SCRIPT" "$@"
