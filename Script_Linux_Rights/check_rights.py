import os
import platform
import ctypes
import subprocess
import getpass

def get_current_user():
    """Récupère le nom de l'utilisateur actuel"""
    try:
        return os.getlogin()
    except Exception:
        try:
            return getpass.getuser()
        except Exception as e:
            print(f"Erreur lors de la récupération de l'utilisateur : {e}")
            return None

def get_groups_linux(user):
    """Récupère les groupes auxquels l'utilisateur appartient"""
    try:
        groups = subprocess.check_output(["groups", user]).decode().strip()
        return groups.split(":")[1].strip().split()
    except subprocess.CalledProcessError:
        print(f"Erreur : Impossible de récupérer les groupes pour l'utilisateur {user}.")
        return []

def check_sudo_linux():
    """Vérifie si l'utilisateur a des droits sudo"""
    try:
        sudo_check = subprocess.run(
            ["sudo", "-n", "true"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return sudo_check.returncode == 0
    except FileNotFoundError:
        return False

def summarize_permissions(root_path):
    """Produit un résumé des permissions sur les dossiers principaux."""
    summary = {
        "lecture": 0,
        "écriture": 0,
        "suppression": 0,
        "erreurs": 0,
        "total": 0,
    }

    for root, dirs, files in os.walk(root_path):
        # Limite aux dossiers de premier niveau pour éviter la profondeur excessive
        if root != root_path:
            break

        for directory in dirs:
            dir_path = os.path.join(root, directory)
            try:
                # Vérification des droits
                if os.access(dir_path, os.R_OK):
                    summary["lecture"] += 1
                if os.access(dir_path, os.W_OK):
                    summary["écriture"] += 1
                if os.access(dir_path, os.W_OK) and os.access(os.path.dirname(dir_path), os.W_OK):
                    summary["suppression"] += 1
                summary["total"] += 1
            except Exception:
                summary["erreurs"] += 1

    return summary

def main():
    # Récupération de l'utilisateur actuel
    current_user = get_current_user()
    if not current_user:
        print("Impossible de déterminer l'utilisateur actuel.")
        return

    # Détection du système d'exploitation
    system = platform.system()

    print(f"Utilisateur : {current_user}")
    print(f"Système d'exploitation : {system}")

    if system == "Linux":
        # Vérifie les droits et les groupes de l'utilisateur
        groups = get_groups_linux(current_user)
        print(f"Groupes de l'utilisateur : {', '.join(groups)}")

        if check_sudo_linux():
            print("L'utilisateur a les droits sudo.")
        else:
            print("L'utilisateur n'a PAS les droits sudo.")

        root_path = "/"  # Racine par défaut pour Linux

    elif system == "Windows":
        # Vérifie les droits administrateurs
        if check_admin_windows():
            print("L'utilisateur a les droits administrateur.")
        else:
            print("L'utilisateur n'a PAS les droits administrateur.")

        root_path = "C:\\"  # Racine par défaut pour Windows
    else:
        print("Système non pris en charge.")
        return

    # Résumé des permissions
    print("\n--- Résumé des permissions sur les dossiers principaux ---")
    summary = summarize_permissions(root_path)
    print(f"Dossiers analysés : {summary['total']}")
    print(f"  Lecture autorisée : {summary['lecture']}")
    print(f"  Écriture autorisée : {summary['écriture']}")
    print(f"  Suppression autorisée : {summary['suppression']}")
    print(f"  Erreurs (accès refusé ou autre) : {summary['erreurs']}")

if __name__ == "__main__":
    main()

