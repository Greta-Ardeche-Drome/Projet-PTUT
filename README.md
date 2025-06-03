# 🚀 Projet PTUT - HawKey 

📅 **Date de début :** 20/10/2024  
📌 **Description :** Ce projet regroupe plusieurs scripts permettant de réaliser des audits de sécurité en local et sur le réseau.

## 📌 Historique des mises à jour

### 🗂️ 20/11/2024 – Scan local des fichiers sensibles
✅ Création d'un script permettant de :
- Vérifier les permissions sur des fichiers sensibles en local.
- Créer un dossier avec un nom personnalisé.
- Générer un rapport daté (jj-mm-aa) dans ce dossier.
  
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
- Récupération des CVE en fonction des versions trouvées.
- Ajout d'un résultat en HTML avec tableau pour simplifier la lecture.

### 🔄 19/03/2025 – Automatisation & Améliorations

✅ Mise à jour de `scan_network.py` pour :
- Ajout du scan des CVE 
- Résultat des CVE dans le rapport en html

### 🔄 27/05/2025 – Ajout du scan logiciel + modificication du scan local et rendu HTML

✅ Mise à jour de `postscanlocal.ps1` sous le nouveau nom de `scan_local_logiciel.py`  pour :
- Intégration du scan local + scan logiciel en même temps
- Améliorations du rapport html pour un meilleur rendu 
---
### 🔄 28/05/2025 – Amélioration du scan réseau
- Améliorations du rapport html pour un meilleur rendu

### 🔄 03/05/2025 – Mise à jour de la documentation READme
- Explication du fonctionnement du scan local + logiciels
## 📂 Contenu du projet
| 📜 Script | 📝 Description |
|-----------|--------------|
| `scan_local_logiciel.py` | Scan local des permissions et fichiers sensibles (Windows) + scan des logiciels sur le poste |
| `scan_network.py` | Scan réseau des machines et des ports ouverts (Windows/Linux) |
| `launcher.ps1` | Script pour automatiser le lancement des scans |
| `requirement.ps1` | Script pour télécharger les prérequis pour la suite (Windows)|


## 🚀 Utilisation

### 🔍 **Exécuter les requirements**
```powershell
.\requirement.ps1
```
### 🛠 **Exécuter les scripts de manière automatiser**
```powershell
.\launcher.ps1
```
### **Le script lancera** : 

-> Scan en local avec .\scan_local_logiciel.py

-> Scan réseau avec .\scan_network.py

-> 2 rapports générés : 
Le premier répertorie l'ensemble du scan des permissions locales ainsi que les logiciels du poste
Le deuxième répertorie toutes les adresses IP du réseau scanné avec les ports + versions des services ainsi que les CVE associés

📌 **Remarque :** Certains scripts nécessitent des **droits administrateurs**.
---
## 🛠️ Technologies utilisées
- **Python** (nmap, psutil, socket, ipaddress)
- **PowerShell** 
---
## 📧 Contact
📌 **Auteur :** Equipe [HawKey]  
📌 **Projet PTUT - 2024/2025**

