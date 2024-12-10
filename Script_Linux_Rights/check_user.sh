#!/bin/bash

# Vérification si Python est installé
echo "Vérification de l'installation de Python..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 n'est pas installé. Installation en cours..."
    # Détection du système d'exploitation
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt &> /dev/null; then
            sudo apt update && sudo apt install -y python3 python3-pip
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3 python3-pip
        elif command -v pacman &> /dev/null; then
            sudo pacman -Syu --noconfirm python python-pip
        else
            echo "Gestionnaire de paquets non pris en charge. Installez Python3 manuellement."
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # MacOS
        if ! command -v brew &> /dev/null; then
            echo "Homebrew n'est pas installé. Installez Homebrew d'abord."
            exit 1
        fi
        brew install python3
    else
        echo "Système d'exploitation non pris en charge pour l'installation automatique de Python."
        exit 1
    fi
else
    echo "Python3 est déjà installé."
fi

# Vérification si le script Python existe
PYTHON_SCRIPT="check_rights.py"

if [[ ! -f "$PYTHON_SCRIPT" ]]; then
    echo "Le fichier $PYTHON_SCRIPT est introuvable. Assurez-vous qu'il est présent dans le même répertoire que ce script."
    exit 1
fi

# Exécution du script Python
echo "Exécution du script Python..."
python3 "$PYTHON_SCRIPT"
