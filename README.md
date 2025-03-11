# 🚀 Projet PTUT

📅 **Date de début :** 20/11/2024  
📌 **Description :** Ce projet regroupe plusieurs scripts permettant de réaliser des audits de sécurité en local et sur le réseau.

## 📌 Historique des mises à jour

### 🗂️ 20/11/2024 – Scan local des fichiers sensibles
✅ Création d'un script permettant de :
- Vérifier les permissions sur des fichiers sensibles en local.
- Créer un dossier avec un nom personnalisé.
- Générer un rapport daté (jj-mm-aa) dans ce dossier.

### 🖥️ 12/12/2024 – Vérification des droits sous Linux/MacOS
✅ Développement d'un script sous Linux/MacOS permettant :
- De vérifier les droits d'un utilisateur en local.
- D'afficher les fichiers sensibles accessibles avec ses permissions.

### 🌐 07/02/2025 – Scan réseau
✅ Mise en place d'un script de scan réseau :
- Récupération des interfaces réseau disponibles.
- Scan d'une carte réseau sélectionnée à partir du masque de sous-réseau.
- Découverte des ports ouverts sur les adresses IP du réseau.

### 🔄 11/03/2025 – Automatisation & Améliorations
✅ Création d'un script **launcher** pour automatiser :
- Le lancement des scripts `postscanlocal.ps1` et `scan_network.py`.

✅ Mise à jour de `scan_network.py` pour :
- Ajouter la détection des **versions des services** sur les ports ouverts.

---

## 📂 Contenu du projet
| 📜 Script | 📝 Description |
|-----------|--------------|
| `postscanlocal.ps1` | Scan local des permissions et fichiers sensibles (Windows) |
| `scan_network.py` | Scan réseau des machines et des ports ouverts (Windows/Linux) |
| `launcher.sh` | Script pour automatiser le lancement des scans |

## 🚀 Utilisation

### 🔍 **Exécuter un scan local**
```powershell
.\postscanlocal.ps1
```

### 🌐 **Exécuter un scan réseau**
```bash
python3 scan_network.py
```

### 🛠 **Automatiser les scans**
```bash
./launcher.sh
```

📌 **Remarque :** Certains scripts nécessitent des **droits administrateurs**.

---

## 🛠️ Technologies utilisées
- **Python** (nmap, psutil, socket, ipaddress)
- **PowerShell** (audit des permissions)
- **Bash** (automation)

---

## 📧 Contact
📌 **Auteur :** [Votre Nom]  
📌 **Email :** [Votre Email]  
📌 **Projet PTUT - 2024/2025**

