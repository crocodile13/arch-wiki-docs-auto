#!/bin/bash

set -e

# Création de l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Mise à jour de pip
pip install --upgrade pip

# Installation des dépendances
pip install requests
