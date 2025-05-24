#!/bin/bash
set -e

# Créer le venv
python3 -m venv venv

# Activer le venv
source venv/bin/activate

# Mettre à jour pip
pip install --upgrade pip

# Installer les dépendances nécessaires
pip install simplemediawiki ArchWiki || echo "⚠️ Assure-toi que le module ArchWiki est installable via pip ou présent localement."

# Lancer le script avec un exemple d'argument
python3 arch-wiki-docs.py --output-directory ./output
