#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HawKey - Audit Local et Logiciels Unifié v2.1
============================================
Script unifié pour l'audit de sécurité local et des logiciels
Génère un rapport HTML consolidé avec design moderne et interactif
"""

import os
import sys
import csv
import json
import time
import winreg
import platform
import datetime
import subprocess
import ctypes
from pathlib import Path

class HawKeyLocalAudit:
    def __init__(self, output_folder="E:/HawKey/Rapport"):
        self.output_folder = output_folder
        self.ensure_output_folder()
        self.audit_results = {
            'system_info': {},
            'local_security': {},
            'software_audit': {},
            'statistics': {}
        }

        # Liste complète des logiciels requis (Mises à jour Mai 2025)
        self.required_software = {
            # Navigateurs Web
            'Google Chrome': '125.0',
            'Mozilla Firefox': '126.0',
            'Microsoft Edge': '125.0',
            'Opera': '110.0',
            'Brave': '1.66',
            'Vivaldi': '6.7',
            'Tor Browser': '13.5',
            'Waterfox': '6.1',
            'Pale Moon': '33.0',

            # Suites Bureautiques
            'Microsoft 365': '16.0.17531',
            'LibreOffice': '24.2',
            'OpenOffice': '4.1.15',
            'WPS Office': '12.1',
            'OnlyOffice': '8.0',

            # Lecteurs PDF
            'Adobe Acrobat Reader DC': '24.2.20857',
            'Foxit PDF Reader': '2024.2',
            'SumatraPDF': '3.6',
            'PDF-XChange Editor': '10.4',
            'Nitro PDF Reader': '15.0',

            # Outils de Communication
            'Microsoft Teams': '24134.3404',
            'Zoom': '5.17.11',
            'Skype': '8.117',
            'TeamViewer': '15.54',
            'AnyDesk': '8.3',
            'Slack': '4.38',
            'Discord': '1.0.9167',
            'Cisco Webex': '44.5',
            'Telegram': '5.2',
            'WhatsApp': '2.2418',
            'Signal': '7.7',

            # Compression et Archives
            '7-Zip': '24.05',
            'WinRAR': '7.01',
            'WinZip': '29.0',
            'PeaZip': '9.8',
            'Bandizip': '7.33',
            'IZArc': '4.6',

            # Utilitaires Système
            'CCleaner': '6.23',
            'CPU-Z': '2.10',
            'GPU-Z': '2.58',
            'HWiNFO': '7.74',
            'Crystal Disk Info': '9.3',
            'Speccy': '1.33',
            'Process Explorer': '17.05',
            'Sysinternals Suite': '2024.05',

            # Multimédia
            'VLC media player': '3.0.21',
            'K-Lite Codec Pack': '18.1',
            'GIMP': '2.10.38',
            'Audacity': '3.5.1',
            'iTunes': '12.13.2',
            'OBS Studio': '30.1.2',
            'HandBrake': '1.8.0',
            'Krita': '5.2.2',
            'Blender': '4.1',

            # Sécurité et Antivirus
            'Malwarebytes': '5.1.6',
            'Avast Free Antivirus': '24.4',
            'AVG AntiVirus Free': '24.4',
            'Bitdefender Total Security': '28.0.4',
            'Windows Defender': '4.18.24040.9',
            'Kaspersky Free': '21.17.19',
            'Norton 360': '22.25.1',
            'ESET NOD32': '17.1',

            # Développement et Programmation
            'Visual Studio Code': '1.89',
            'Notepad++': '8.7',
            'Git': '2.45',
            'Python': '3.12.3',
            'Node.js': '22.2',
            'FileZilla': '3.67',
            'PuTTY': '0.81',
            'WinSCP': '6.3.3',
            'Postman': '11.2',
            'Eclipse IDE': '2024-06',
            'IntelliJ IDEA': '2024.1',
            'Visual Studio': '17.10',
            'Docker Desktop': '4.30',

            # Virtualisation
            'VirtualBox': '7.0.18',
            'VMware Workstation Pro': '17.5.2',
            'VMware Player': '17.5.2',
            'Hyper-V': '10.0.22621',

            # Java Runtime
            'Java 8': '8.0.411',
            'Java 11': '11.0.23',
            'Java 17': '17.0.11',
            'Java 21': '21.0.3',
            'OpenJDK': '22.0.1',

            # Bases de Données et Outils
            'MySQL Workbench': '8.0.37',
            'DBeaver': '24.0.5',
            'PostgreSQL': '16.3',
            'MongoDB Compass': '1.43',
            'HeidiSQL': '12.7',
            'SQLite Browser': '3.12.2',
            'phpMyAdmin': '5.2.1',

            # Outils Réseau et Analyse
            'Wireshark': '4.2.5',
            'Advanced IP Scanner': '2.6.3850',
            'NetWorx': '7.1.1',
            'Nmap': '7.95',
            'Fiddler Classic': '5.0.20231.10049',
            'Angry IP Scanner': '3.9.1',
            'Advanced Port Scanner': '2.5.3977',
            'Network Scanner': '8.4',

            # Clients Email
            'Mozilla Thunderbird': '115.11.0',
            'Microsoft Outlook': '16.0.17531',
            'eM Client': '10.1.4588',
            'Mailbird': '2.9.84',

            # Outils de Sauvegarde et Récupération
            'Macrium Reflect Free': '8.1.7531',
            'AOMEI Backupper': '8.0.1',
            'EaseUS Todo Backup': '16.0',
            'Clonezilla': '3.1.2',
            'Acronis True Image': '2024',
            'Veeam Agent': '6.1',

            # Support à Distance et VPN
            'Remote Desktop Connection': '10.1.2048',
            'UltraVNC': '1.4.40',
            'TightVNC': '2.8.85',
            'NoMachine': '8.13',
            'Chrome Remote Desktop': '125.0',
            'OpenVPN': '2.6.10',
            'WireGuard': '0.5.3',

            # Outils de Productivité
            'Notion': '3.13',
            'Trello': '1.116',
            'Todoist': '9.0.11',
            'Evernote': '10.97',
            'OneNote': '16.0.17531',
            'Adobe Creative Cloud': '6.2.0',

            # Lecteurs et Visionneuses
            'IrfanView': '4.67',
            'FastStone Image Viewer': '7.8',
            'XnView': '2.52',
            'Adobe Flash Player': '34.0.0.267',
            'Shockwave Player': '12.3.5.205',

            # Outils de Système et Maintenance
            'Revo Uninstaller': '2.4.5',
            'IObit Uninstaller': '13.5',
            'Glary Utilities': '6.13',
            'Wise Care 365': '6.7.2',
            'Advanced SystemCare': '17.4',

            # Clients Cloud et Stockage
            'Dropbox': '201.4.5551',
            'Google Drive': '90.0.2',
            'OneDrive': '24.086.0428',
            'iCloud': '15.0.0.42',
            'Box Drive': '2.38',

            # Outils de Streaming et Gaming
            'Steam': '1718817212',
            'Epic Games Launcher': '15.17.1',
            'Origin': '10.5.135',
            'Ubisoft Connect': '141.0.10857',
            'GOG Galaxy': '2.0.74',
            'Twitch': '9.0.1',

            # Messagerie Instantanée Professionnelle
            'Microsoft Teams Classic': '1.7.00.8773',
            'Slack Desktop': '4.38.125',
            'Discord Canary': '1.0.400',
            'Mattermost': '5.8.0',
            'Rocket.Chat': '3.9.7',

            # Outils de Design et Créativité
            'Canva': '1.91.0',
            'Figma': '116.16.8',
            'Sketch': '100.3',
            'Adobe Photoshop': '25.9.1',
            'Adobe Illustrator': '28.5',
            'Inkscape': '1.3.2',

            # Navigateurs Spécialisés
            'Brave Browser': '1.66.118',
            'DuckDuckGo Browser': '1.80.0',
            'LibreWolf': '126.0',

            # Outils de Test et Qualité
            'Selenium WebDriver': '4.21.0',
            'JMeter': '5.6.3',
            'LoadRunner': '2024',
            'Burp Suite': '2024.5.2',
            'OWASP ZAP': '2.15.0'
        }

        # Définition des aliases pour les noms de logiciels
        self.software_aliases = {
            'Google Chrome': ['Chrome', 'GoogleChrome', 'Google Chrome Browser'],
            'Microsoft Edge': ['Edge', 'MSEdge', 'Microsoft Edge WebView2'],
            'Mozilla Firefox': ['Firefox', 'Mozilla Firefox ESR'],
            'Visual Studio Code': ['VS Code', 'VSCode', 'Code'],
            'Microsoft 365': ['Office 365', 'Microsoft Office', 'Office'],
            'Adobe Acrobat Reader DC': ['Adobe Reader', 'Acrobat Reader', 'Adobe Acrobat'],
            'VLC media player': ['VLC', 'VideoLAN VLC media player'],
            'Python': ['Python 3', 'Python 3.12'],
            'MongoDB Compass': ['MongoDB', 'Compass'],
            'Wireshark': ['Wireshark Network Analyzer'],
            'Microsoft Teams': ['Teams', 'Microsoft Teams classic'],
            '7-Zip': ['7-Zip File Manager', '7-Zip GUI'],
            'Docker Desktop': ['Docker'],
            'Node.js': ['Node', 'nodejs'],
            'Git': ['Git for Windows'],
            'Java 8': ['Java 8 Update', 'Java SE Runtime Environment 8'],
            'Java 11': ['Java 11 LTS', 'Java SE Development Kit 11'],
            'Java 17': ['Java 17 LTS', 'Java SE Development Kit 17'],
            'Java 21': ['Java 21 LTS', 'Java SE Development Kit 21'],
            'Windows Defender': ['Microsoft Defender', 'Windows Security'],
            'Remote Desktop Connection': ['Remote Desktop', 'mstsc'],
            'Notepad++': ['Notepad Plus Plus'],
            'CCleaner': ['CCleaner Free', 'CCleaner Professional'],
            'iTunes': ['Apple iTunes'],
            'Skype': ['Skype for Windows'],
            'TeamViewer': ['TeamViewer 15'],
            'Zoom': ['Zoom Client', 'Zoom Meetings'],
            'WinRAR': ['WinRAR archiver'],
            'Malwarebytes': ['Malwarebytes Anti-Malware'],
            'VirtualBox': ['Oracle VM VirtualBox'],
            'VMware Workstation Pro': ['VMware Workstation'],
            'Dropbox': ['Dropbox Update Helper'],
            'Steam': ['Steam Client'],
            'Discord': ['Discord Inc'],
            'Telegram': ['Telegram Desktop'],
            'WhatsApp': ['WhatsApp Desktop'],
            'Slack': ['Slack Technologies'],
            'GIMP': ['GNU Image Manipulation Program'],
            'Audacity': ['Audacity audio editor'],
            'HandBrake': ['HandBrake Video Transcoder'],
            'OBS Studio': ['OBS'],
            'FileZilla': ['FileZilla Client'],
            'PuTTY': ['PuTTY SSH client'],
            'WinSCP': ['WinSCP SFTP client'],
            'Postman': ['Postman API Platform'],
            'IntelliJ IDEA': ['IntelliJ'],
            'Eclipse IDE': ['Eclipse', 'Eclipse IDE for Java Developers'],
            'Visual Studio': ['Microsoft Visual Studio'],
            'Mozilla Thunderbird': ['Thunderbird'],
            'Microsoft Outlook': ['Outlook'],
            'OneNote': ['Microsoft OneNote'],
            'Adobe Photoshop': ['Photoshop'],
            'Adobe Illustrator': ['Illustrator'],
            'Blender': ['Blender 3D'],
            'Krita': ['Krita Digital Painting'],
            'LibreOffice': ['LibreOffice Writer', 'LibreOffice Calc'],
            'OpenOffice': ['Apache OpenOffice']
        }

    def ensure_output_folder(self):
        """Créer le dossier de sortie"""
        try:
            os.makedirs(self.output_folder, exist_ok=True)
        except Exception as e:
            print(f"Erreur création dossier: {e}")

    def is_admin(self):
        """Vérifier les droits administrateur"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False

    def get_system_info(self):
        """Collecter les informations système"""
        print("[INFO] 🖥️ Collecte des informations système...")

        try:
            self.audit_results['system_info'] = {
                'computer_name': platform.node(),
                'username': os.getenv('USERNAME'),
                'domain': os.getenv('USERDOMAIN'),
                'os_name': platform.system(),
                'os_version': platform.version(),
                'os_release': platform.release(),
                'architecture': platform.architecture()[0],
                'is_admin': self.is_admin(),
                'scan_date': datetime.datetime.now().isoformat()
            }
            print("✅ Informations système collectées")
        except Exception as e:
            print(f"❌ Erreur collecte système: {e}")

    def get_admin_users(self):
        """Récupérer les utilisateurs administrateurs"""
        print("[INFO] 👥 Analyse des utilisateurs administrateurs...")

        admin_users = []
        try:
            cmd = 'net localgroup Administrateurs'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='cp850')

            if result.returncode == 0:
                lines = result.stdout.splitlines()
                in_members = False
                for line in lines:
                    line = line.strip()
                    if "membres" in line.lower() or "members" in line.lower():
                        in_members = True
                        continue
                    elif "La commande" in line or "The command" in line:
                        break
                    elif in_members and line and not line.startswith('-'):
                        admin_users.append({
                            'name': line,
                            'source': 'Local'
                        })

            if not admin_users and self.is_admin():
                current_user = os.getenv('USERNAME', 'Current User')
                admin_users.append({
                    'name': current_user,
                    'source': 'Current Session'
                })

            print(f"✅ {len(admin_users)} administrateur(s) trouvé(s)")

        except Exception as e:
            print(f"❌ Erreur récupération admins: {e}")
            admin_users.append({
                'name': os.getenv('USERNAME', 'Unknown'),
                'source': 'Current Session (Fallback)'
            })

        return admin_users

    def check_folder_permissions(self):
        """Vérifier les permissions des dossiers critiques"""
        print("[INFO] 🔒 Vérification des permissions...")

        critical_folders = [
            "C:\\Windows",
            "C:\\Windows\\System32",
            "C:\\Program Files",
            "C:\\Program Files (x86)",
            "C:\\Users",
            "C:\\Windows\\Temp"
        ]

        folder_permissions = []

        for folder in critical_folders:
            print(f"  📁 Vérification: {folder}")

            try:
                permissions_data = {
                    'folder': folder,
                    'status': 'accessible' if os.path.exists(folder) else 'inaccessible',
                    'permissions': [],
                    'issues': []
                }

                if os.path.exists(folder):
                    try:
                        test_files = os.listdir(folder)[:3]
                        permissions_data['permissions'].append(f"✅ Lecture autorisée ({len(test_files)} fichiers visibles)")

                        test_file = os.path.join(folder, "hawkey_test.tmp")
                        try:
                            with open(test_file, 'w') as f:
                                f.write("test")
                            os.remove(test_file)
                            permissions_data['issues'].append("⚠️ Écriture autorisée - Risque de sécurité")
                        except (PermissionError, OSError):
                            permissions_data['permissions'].append("✅ Écriture protégée")

                    except PermissionError:
                        permissions_data['permissions'].append("🔒 Accès restreint (sécurisé)")
                    except Exception as e:
                        permissions_data['issues'].append(f"❌ Erreur: {str(e)[:40]}...")

                try:
                    cmd = f'icacls "{folder}"'
                    result = subprocess.run(cmd, shell=True, capture_output=True,
                                          text=True, encoding='cp850', timeout=2)

                    if result.returncode == 0 and result.stdout:
                        lines = result.stdout.splitlines()[:3]
                        for line in lines:
                            if ':' in line and len(line) < 100:
                                permissions_data['permissions'].append(line.strip()[:60] + "...")

                        stdout_lower = result.stdout.lower()
                        if 'everyone:(f)' in stdout_lower or 'tout le monde:(f)' in stdout_lower:
                            permissions_data['issues'].append("🚨 Permissions Everyone complètes!")
                        if 'users:(f)' in stdout_lower or 'utilisateurs:(f)' in stdout_lower:
                            permissions_data['issues'].append("⚠️ Permissions Users complètes!")

                except subprocess.TimeoutExpired:
                    permissions_data['permissions'].append("⏰ Vérification interrompue (timeout)")
                except Exception:
                    permissions_data['permissions'].append("ℹ️ Vérification icacls indisponible")

                folder_permissions.append(permissions_data)

            except Exception as e:
                folder_permissions.append({
                    'folder': folder,
                    'status': 'error',
                    'permissions': [],
                    'issues': [f"❌ Erreur: {str(e)[:50]}..."]
                })

        print(f"✅ Permissions vérifiées pour {len(critical_folders)} dossiers")
        return folder_permissions

    def get_software_audit(self):
        """Audit des logiciels (liste complète restaurée)"""
        print("[INFO] 📦 Audit des logiciels installés...")

        software_results = []
        installed_software = self.get_installed_software()

        total = len(self.required_software)
        progress = 0

        for software, required_version in self.required_software.items():
            progress += 1
            percentage = round((progress / total) * 100)
            print(f"\r  📦 Progression: {percentage}% - {software[:30]}...", end="", flush=True)

            installed = self.find_software_match(installed_software, software)

            if installed:
                version_ok = self.compare_versions(installed['DisplayVersion'], required_version)
                software_results.append({
                    'software': software,
                    'installed': True,
                    'current_version': installed['DisplayVersion'],
                    'required_version': required_version,
                    'up_to_date': version_ok,
                    'status': 'Conforme' if version_ok else 'Obsolète'
                })
            else:
                software_results.append({
                    'software': software,
                    'installed': False,
                    'current_version': 'Non installé',
                    'required_version': required_version,
                    'up_to_date': False,
                    'status': 'Non installé'
                })

        print(f"\n✅ Audit de {len(self.required_software)} logiciels terminé")
        return software_results

    def get_installed_software(self):
        """Récupérer la liste des logiciels installés"""
        software = []

        reg_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall")
        ]

        for reg_hive, reg_path in reg_paths:
            try:
                reg_key = winreg.OpenKey(reg_hive, reg_path)

                for i in range(winreg.QueryInfoKey(reg_key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(reg_key, i)
                        subkey = winreg.OpenKey(reg_key, subkey_name)

                        try:
                            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            display_version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]

                            if display_name and display_version:
                                software.append({
                                    'DisplayName': display_name,
                                    'DisplayVersion': display_version
                                })
                        except:
                            pass
                        finally:
                            winreg.CloseKey(subkey)
                    except:
                        pass

                winreg.CloseKey(reg_key)
            except:
                continue

        # Recherche des applications Windows Store
        try:
            result = subprocess.run(
                ["powershell", "-Command", "Get-AppxPackage | Select-Object Name, Version | ConvertTo-Json"],
                capture_output=True, text=True, encoding='utf-8'
            )

            if result.returncode == 0:
                appx_data = json.loads(result.stdout)

                if isinstance(appx_data, dict):
                    appx_data = [appx_data]

                for package in appx_data:
                    if package.get('Name') and package.get('Version'):
                        software.append({
                            'DisplayName': package['Name'],
                            'DisplayVersion': package['Version']
                        })
        except:
            pass

        return software

    def find_software_match(self, installed_list, software_name):
        """Trouver un logiciel dans la liste avec alias étendus"""

        # Recherche directe
        matches = [s for s in installed_list if s['DisplayName'] == software_name]

        if not matches:
            matches = [s for s in installed_list
                      if software_name.lower() in s['DisplayName'].lower()
                      or s['DisplayName'].lower() in software_name.lower()]

        if not matches and software_name in self.software_aliases:
            for alias in self.software_aliases[software_name]:
                alias_matches = [s for s in installed_list
                               if alias.lower() in s['DisplayName'].lower()
                               or s['DisplayName'].lower() in alias.lower()]
                if alias_matches:
                    matches = alias_matches
                    break

        if matches and len(matches) > 1:
            try:
                def get_version_key(item):
                    try:
                        version_str = ''.join([c for c in item['DisplayVersion'] if c.isdigit() or c == '.'])
                        parts = version_str.split('.')
                        parts = [int(p) for p in parts if p]
                        while len(parts) < 4:
                            parts.append(0)
                        return parts
                    except:
                        return [0, 0, 0, 0]

                matches.sort(key=get_version_key, reverse=True)
                return matches[0]
            except Exception as e:
                return matches[0]

        return matches[0] if matches else None

    def compare_versions(self, installed, required):
        """Comparer les versions"""
        try:
            installed_clean = ''.join([c for c in installed if c.isdigit() or c == '.'])
            required_clean = ''.join([c for c in required if c.isdigit() or c == '.'])

            if not installed_clean or not required_clean:
                return False

            installed_parts = [int(p) for p in installed_clean.split('.') if p]
            required_parts = [int(p) for p in required_clean.split('.') if p]

            for i in range(max(len(installed_parts), len(required_parts))):
                installed_segment = installed_parts[i] if i < len(installed_parts) else 0
                required_segment = required_parts[i] if i < len(required_parts) else 0

                if installed_segment > required_segment:
                    return True
                elif installed_segment < required_segment:
                    return False

            return True

        except Exception as e:
            return False

    def calculate_statistics(self):
        """Calculer les statistiques"""
        stats = {
            'security_score': 85,
            'total_issues': 0,
            'critical_issues': 0,
            'software_compliance': 0,
            'permission_issues': 0
        }

        if 'folder_permissions' in self.audit_results['local_security']:
            for folder in self.audit_results['local_security']['folder_permissions']:
                stats['permission_issues'] += len(folder.get('issues', []))

        if 'software_results' in self.audit_results['software_audit']:
            total_soft = len(self.audit_results['software_audit']['software_results'])
            installed_soft = len([s for s in self.audit_results['software_audit']['software_results'] if s['installed']])
            ok_soft = len([s for s in self.audit_results['software_audit']['software_results']
                          if s['installed'] and s['up_to_date']])

            if installed_soft > 0:
                stats['software_compliance'] = round((ok_soft / installed_soft) * 100, 1)

        stats['total_issues'] = stats['permission_issues']
        if stats['permission_issues'] > 5:
            stats['security_score'] -= 20
        elif stats['permission_issues'] > 2:
            stats['security_score'] -= 10

        if stats['software_compliance'] < 70:
            stats['security_score'] -= 15
            stats['critical_issues'] += 1

        self.audit_results['statistics'] = stats

    def run_full_audit(self):
        """Lancer l'audit complet"""
        print("\n" + "="*60)
        print("🔍 HAWKEY - AUDIT LOCAL ET LOGICIELS v2.1")
        print("="*60)

        if not self.is_admin():
            print("⚠️ Ce script nécessite des droits d'administrateur pour un audit complet.")
            response = input("Continuer quand même? (O/N): ")
            if response.upper() != 'O':
                return False

        start_time = time.time()

        self.get_system_info()

        print("\n[PHASE 1] 🔒 Audit de sécurité local")
        admin_users = self.get_admin_users()
        folder_permissions = self.check_folder_permissions()

        self.audit_results['local_security'] = {
            'admin_users': admin_users,
            'folder_permissions': folder_permissions
        }

        print("\n[PHASE 2] 📦 Audit des logiciels")
        software_results = self.get_software_audit()

        self.audit_results['software_audit'] = {
            'software_results': software_results
        }

        self.calculate_statistics()

        print("\n[PHASE 3] 📄 Génération du rapport")
        report_path = self.generate_html_report()

        elapsed_time = time.time() - start_time

        print(f"\n{'='*60}")
        print("📊 RÉSUMÉ DE L'AUDIT")
        print(f"{'='*60}")
        print(f"⏱️  Durée: {elapsed_time:.2f} secondes")
        print(f"🔒 Score sécurité: {self.audit_results['statistics']['security_score']}/100")
        print(f"📦 Conformité logiciels: {self.audit_results['statistics']['software_compliance']}%")
        print(f"⚠️  Problèmes détectés: {self.audit_results['statistics']['total_issues']}")
        print(f"📄 Rapport: {report_path}")
        print(f"{'='*60}")

        try:
            if platform.system() == "Windows":
                os.startfile(report_path)
                print("🌐 Rapport ouvert dans le navigateur")
        except:
            print("📄 Ouvrez manuellement le rapport")

        return True

    def generate_html_report(self):
        """Générer le rapport HTML unifié avec design moderne et interactif"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_folder, f"hawkey_audit_unified_{timestamp}.html")

        system_info = self.audit_results['system_info']
        local_security = self.audit_results['local_security']
        software_audit = self.audit_results['software_audit']
        stats = self.audit_results['statistics']

        software_results = software_audit.get('software_results', [])
        installed_count = len([s for s in software_results if s['installed']])
        up_to_date_count = len([s for s in software_results if s['installed'] and s['up_to_date']])
        outdated_count = len([s for s in software_results if s['installed'] and not s['up_to_date']])
        missing_count = len([s for s in software_results if not s['installed']])

        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HawKey - Audit Local et Logiciels v2.1</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }}
        .header p {{ font-size: 1.2em; opacity: 0.9; }}
        .content {{ padding: 30px; }}

        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .summary-card {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        .summary-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        }}
        .summary-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }}
        .summary-card h3 {{
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 2.2em;
            font-weight: 700;
        }}
        .summary-card p {{
            color: #495057;
            font-weight: 600;
            font-size: 1.1em;
        }}

        .success-card {{ border-left: 4px solid #28a745; }}
        .warning-card {{ border-left: 4px solid #ffc107; }}
        .danger-card {{ border-left: 4px solid #dc3545; }}
        .info-card {{ border-left: 4px solid #17a2b8; }}

        .section {{
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
            margin-bottom: 25px;
            border-radius: 12px;
            padding: 25px;
            border: 1px solid #dee2e6;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }}
        .section h2 {{
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 3px solid #007bff;
            font-size: 1.8em;
            font-weight: 600;
        }}

        .filters {{
            margin-bottom: 25px;
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            justify-content: center;
        }}
        .filter-btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9em;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .filter-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        .filter-btn.active {{
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
        }}
        .filter-all {{ background: linear-gradient(135deg, #007bff, #0056b3); color: white; }}
        .filter-success {{ background: linear-gradient(135deg, #28a745, #1e7e34); color: white; }}
        .filter-warning {{ background: linear-gradient(135deg, #ffc107, #e0a800); color: #212529; }}
        .filter-danger {{ background: linear-gradient(135deg, #dc3545, #c82333); color: white; }}

        .table-container {{
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            background: linear-gradient(135deg, #495057 0%, #6c757d 100%);
            color: white;
            padding: 15px 12px;
            text-align: left;
            font-weight: 600;
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #dee2e6;
            vertical-align: middle;
        }}
        tr:hover {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            transform: scale(1.01);
            transition: all 0.2s ease;
        }}

        .status-badge {{
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .status-conforme {{
            background: linear-gradient(135deg, #d4edda, #c3e6cb);
            color: #155724;
        }}
        .status-obsolete {{
            background: linear-gradient(135deg, #fff3cd, #ffeaa7);
            color: #856404;
        }}
        .status-missing {{
            background: linear-gradient(135deg, #f8d7da, #f5c6cb);
            color: #721c24;
        }}
        .status-ok {{
            background: linear-gradient(135deg, #d4edda, #c3e6cb);
            color: #155724;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .status-warning {{
            background: linear-gradient(135deg, #fff3cd, #ffeaa7);
            color: #856404;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .status-error {{
            background: linear-gradient(135deg, #f8d7da, #f5c6cb);
            color: #721c24;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }}
        .info-item {{
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #17a2b8;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s ease;
        }}
        .info-item:hover {{
            transform: translateY(-3px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        .info-item strong {{
            color: #2c3e50;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .permissions-box {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            max-height: 200px;
            overflow-y: auto;
            border: 1px solid #dee2e6;
        }}

        .footer {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 25px;
            text-align: center;
            color: #6c757d;
            border-top: 1px solid #dee2e6;
        }}
        .footer p {{
            margin: 5px 0;
            font-weight: 500;
        }}

        .search-box {{
            margin-bottom: 20px;
            padding: 10px;
            border: 2px solid #dee2e6;
            border-radius: 25px;
            font-size: 16px;
            width: 100%;
            max-width: 400px;
            transition: all 0.3s ease;
        }}
        .search-box:focus {{
            outline: none;
            border-color: #007bff;
            box-shadow: 0 0 10px rgba(0,123,255,0.3);
        }}

        .progress-bar {{
            background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .progress-fill {{
            height: 20px;
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 0.85em;
        }}

        @media (max-width: 768px) {{
            .summary-grid {{ grid-template-columns: 1fr; }}
            .info-grid {{ grid-template-columns: 1fr; }}
            .filters {{ justify-content: center; }}
            table {{ font-size: 14px; }}
            .header h1 {{ font-size: 2em; }}
            .content {{ padding: 20px; }}
            .search-box {{ max-width: 100%; }}
        }}
    </style>
    <script>
        function filterTable(status) {{
            const rows = document.querySelectorAll('tbody tr');
            const buttons = document.querySelectorAll('.filter-btn');

            buttons.forEach(btn => btn.classList.remove('active'));
            document.querySelector('.filter-' + status).classList.add('active');

            rows.forEach(row => {{
                const statusCell = row.cells[1].textContent.toLowerCase();
                if (status === 'all') {{
                    row.style.display = '';
                }} else if (status === 'success' && statusCell.includes('conforme')) {{
                    row.style.display = '';
                }} else if (status === 'warning' && statusCell.includes('obsolète')) {{
                    row.style.display = '';
                }} else if (status === 'danger' && (statusCell.includes('non installé') || statusCell.includes('installé'))) {{
                    row.style.display = '';
                }} else {{
                    row.style.display = 'none';
                }}
            }});

            updateVisibleCount();
        }}

        function searchTable() {{
            const input = document.getElementById('searchInput');
            const filter = input.value.toLowerCase();
            const rows = document.querySelectorAll('tbody tr');

            rows.forEach(row => {{
                const text = row.textContent.toLowerCase();
                if (text.includes(filter)) {{
                    row.style.display = '';
                }} else {{
                    row.style.display = 'none';
                }}
            }});

            updateVisibleCount();
        }}

        function updateVisibleCount() {{
            const visibleRows = document.querySelectorAll('tbody tr[style=""], tbody tr:not([style])');
            const countElement = document.getElementById('visibleCount');
            if (countElement) {{
                countElement.textContent = visibleRows.length;
            }}
        }}

        function expandPermissions(element) {{
            const box = element.nextElementSibling;
            if (box.style.maxHeight === 'none') {{
                box.style.maxHeight = '200px';
                element.textContent = '🔍 Voir plus';
            }} else {{
                box.style.maxHeight = 'none';
                element.textContent = '🔼 Voir moins';
            }}
        }}

        window.onload = function() {{
            document.querySelector('.filter-all').classList.add('active');
            updateVisibleCount();
        }}
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ HawKey - Scan Local </h1>
            <p>Rapport consolidé de sécurité système et logiciels - Version Premium</p>
            <div style="margin-top: 15px; font-size: 0.9em; opacity: 0.8;">
                🔍 {len(software_results)} logiciels analysés | 📊 Analyse approfondie | ⚡ Scan optimisé
            </div>
        </div>

        <div class="content">
            <!-- Résumé Exécutif Premium -->
            <div class="summary-grid">
                <div class="summary-card {'success-card' if stats['security_score'] >= 80 else 'warning-card' if stats['security_score'] >= 60 else 'danger-card'}">
                    <h3>{stats['security_score']}/100</h3>
                    <p>Score de Sécurité</p>
                    <div class="progress-bar" style="margin-top: 10px;">
                        <div class="progress-fill" style="width: {stats['security_score']}%;">
                            {stats['security_score']}%
                        </div>
                    </div>
                </div>
                <div class="summary-card {'success-card' if up_to_date_count == installed_count else 'warning-card'}">
                    <h3>{up_to_date_count}/{installed_count}</h3>
                    <p>Logiciels Conformes</p>
                    <div class="progress-bar" style="margin-top: 10px;">
                        <div class="progress-fill" style="width: {round((up_to_date_count/installed_count*100), 1) if installed_count > 0 else 0}%;">
                            {round((up_to_date_count/installed_count*100), 1) if installed_count > 0 else 0}%
                        </div>
                    </div>
                </div>
                <div class="summary-card {'success-card' if outdated_count == 0 else 'danger-card' if outdated_count > 10 else 'warning-card'}">
                    <h3>{outdated_count}</h3>
                    <p>Versions Obsolètes</p>
                </div>
                <div class="summary-card {'success-card' if stats['permission_issues'] == 0 else 'warning-card'}">
                    <h3>{stats['permission_issues']}</h3>
                    <p>Problèmes Permissions</p>
                </div>
            </div>

            <!-- Informations Système Premium -->
            <div class="section">
                <h2>🖥️ Informations Système</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <strong>💻 Ordinateur:</strong><br>{system_info.get('computer_name', 'Unknown')}
                    </div>
                    <div class="info-item">
                        <strong>👤 Utilisateur:</strong><br>{system_info.get('username', 'Unknown')}
                    </div>
                    <div class="info-item">
                        <strong>🏢 Domaine:</strong><br>{system_info.get('domain', 'Unknown')}
                    </div>
                    <div class="info-item">
                        <strong>🖥️ Système:</strong><br>{system_info.get('os_name', 'Unknown')} {system_info.get('os_release', '')}
                    </div>
                    <div class="info-item">
                        <strong>🔧 Architecture:</strong><br>{system_info.get('architecture', 'Unknown')}
                    </div>
                    <div class="info-item">
                        <strong>🛡️ Admin:</strong><br>{'✅ Oui' if system_info.get('is_admin') else '❌ Non'}
                    </div>
                </div>
            </div>

            <!-- Utilisateurs Administrateurs -->
            <div class="section">
                <h2>👥 Utilisateurs Administrateurs ({len(local_security.get('admin_users', []))})</h2>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Nom d'utilisateur</th>
                                <th>Source</th>
                                <th>Statut</th>
                            </tr>
                        </thead>
                        <tbody>"""

        for user in local_security.get('admin_users', []):
            source = user.get('source', 'Unknown')
            status_class = "status-ok" if source != 'Erreur' else "status-error"
            html += f"""
                            <tr>
                                <td><strong>{user.get('name', 'Unknown')}</strong></td>
                                <td>{source}</td>
                                <td><span class="{status_class}">{'✅ Valide' if source != 'Erreur' else '❌ Erreur'}</span></td>
                            </tr>"""

        html += f"""
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Audit des Logiciels avec Filtres Améliorés -->
            <div class="section">
                <h2>📦 Audit des Logiciels</h2>

                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 15px;">
                    <input type="text" id="searchInput" class="search-box" placeholder="🔍 Rechercher un logiciel..." onkeyup="searchTable()">
                    <div style="color: #6c757d; font-weight: 500;">
                        <span id="visibleCount">{len(software_results)}</span> logiciel(s) affiché(s)
                    </div>
                </div>

                <div class="filters">
                    <button class="filter-btn filter-all" onclick="filterTable('all')">
                        Tous ({len(software_results)})
                    </button>
                    <button class="filter-btn filter-success" onclick="filterTable('success')">
                        ✅ Conformes ({up_to_date_count})
                    </button>
                    <button class="filter-btn filter-warning" onclick="filterTable('warning')">
                        ⚠️ Obsolètes ({outdated_count})
                    </button>
                    <button class="filter-btn filter-danger" onclick="filterTable('danger')">
                        ❌ Non Installés ({missing_count})
                    </button>
                </div>

                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Logiciel</th>
                                <th>Statut</th>
                                <th>Version Installée</th>
                                <th>Version Minimale</th>
                                <th>Action Recommandée</th>
                            </tr>
                        </thead>
                        <tbody>"""

        software_sorted = sorted(software_results, key=lambda x: (
            0 if x['status'] == 'Conforme' else 1 if x['status'] == 'Obsolète' else 2,
            x['software']
        ))

        for software in software_sorted:
            if software['status'] == 'Conforme':
                status_class = "status-conforme"
                action = "✅ Aucune action requise"
            elif software['status'] == 'Obsolète':
                status_class = "status-obsolete"
                action = "⚠️ Mise à jour requise"
            else:
                status_class = "status-missing"
                action = "📥 Rien à signaler"

            html += f"""
                            <tr>
                                <td><strong>{software['software']}</strong></td>
                                <td><span class="{status_class}">{software['status']}</span></td>
                                <td><code style="background: #f8f9fa; padding: 2px 6px; border-radius: 4px;">{software['current_version']}</code></td>
                                <td><code style="background: #f8f9fa; padding: 2px 6px; border-radius: 4px;">{software['required_version']}</code></td>
                                <td>{action}</td>
                            </tr>"""

        html += """
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Permissions des Dossiers Améliorées -->
            <div class="section">
                <h2>🔒 Analyse des Permissions Système</h2>"""

        for folder_data in local_security.get('folder_permissions', []):
            folder_path = folder_data.get('folder', 'Unknown')
            status = folder_data.get('status', 'unknown')
            issues = folder_data.get('issues', [])
            permissions = folder_data.get('permissions', [])

            status_class = "success-card" if status == 'accessible' and not issues else "warning-card" if status == 'accessible' else "danger-card"
            status_text = "✅ Sécurisé" if status == 'accessible' and not issues else "⚠️ Attention" if issues else "❌ Erreur"

            html += f"""
                <div style="margin-bottom: 20px; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" class="{status_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <h3 style="margin: 0; color: #2c3e50; font-size: 1.2em;">📁 {folder_path}</h3>
                        <span class="status-{'ok' if not issues else 'warning' if status == 'accessible' else 'error'}">{status_text}</span>
                    </div>"""

            if issues:
                html += '<div style="background: linear-gradient(135deg, #fff3cd, #ffeaa7); padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #ffc107;">'
                html += '<h4 style="color: #856404; margin-bottom: 10px;">⚠️ Problèmes détectés:</h4>'
                for issue in issues:
                    html += f"<p style='margin: 8px 0; color: #856404; font-weight: 500;'>• {issue}</p>"
                html += "</div>"

            if permissions:
                html += f'<button onclick="expandPermissions(this)" style="background: #17a2b8; color: white; border: none; padding: 8px 16px; border-radius: 20px; cursor: pointer; margin: 10px 0; font-weight: 500;">🔍 Voir permissions</button>'
                html += '<div class="permissions-box" style="margin-top: 10px;">'
                html += f"<strong>Permissions détectées ({len(permissions)}):</strong><br><br>"
                for perm in permissions[:5]:
                    html += f"{perm}<br>"
                if len(permissions) > 5:
                    html += f"<br><em style='color: #6c757d;'>... et {len(permissions) - 5} permission(s) supplémentaire(s)</em>"
                html += "</div>"

            html += "</div>"

        html += """
            </div>

            <!-- Recommandations de Sécurité Améliorées -->
            <div class="section">
                <h2>🎯 Recommandations Personnalisées</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px;">"""

        recommendations = []

        if stats['security_score'] < 70:
            recommendations.append({
                'title': '🚨 Score de Sécurité Critique',
                'desc': f'Votre score de {stats["security_score"]}/100 nécessite une attention immédiate. Priorisez les actions correctives.',
                'priority': 'critical',
                'action': 'Corriger immédiatement'
            })

        if outdated_count > 10:
            recommendations.append({
                'title': '⚠️ Nombreux Logiciels Obsolètes',
                'desc': f'{outdated_count} logiciels nécessitent une mise à jour. Risque élevé de vulnérabilités.',
                'priority': 'high',
                'action': 'Planifier les mises à jour'
            })
        elif outdated_count > 0:
            recommendations.append({
                'title': '📈 Logiciels à Mettre à Jour',
                'desc': f'{outdated_count} logiciel(s) obsolète(s) détecté(s). Maintenance recommandée.',
                'priority': 'medium',
                'action': 'Mise à jour recommandée'
            })

        if stats['permission_issues'] > 2:
            recommendations.append({
                'title': '🔒 Permissions Sensibles Multiples',
                'desc': f'{stats["permission_issues"]} problèmes de permissions détectés sur les dossiers système.',
                'priority': 'high',
                'action': 'Audit des permissions'
            })
        elif stats['permission_issues'] > 0:
            recommendations.append({
                'title': '🔐 Vérification des Permissions',
                'desc': 'Quelques permissions potentiellement dangereuses ont été détectées.',
                'priority': 'medium',
                'action': 'Contrôle recommandé'
            })

        if installed_count < len(software_results) * 0.3:
            recommendations.append({
                'title': '📦 Couverture Logicielle Faible',
                'desc': f'Seulement {installed_count} logiciels installés sur {len(software_results)} recommandés.',
                'priority': 'low',
                'action': 'Évaluer les besoins'
            })

        recommendations.extend([
            {
                'title': '🔄 Audits Réguliers',
                'desc': 'Effectuez cet audit mensuellement pour maintenir un niveau de sécurité optimal.',
                'priority': 'low',
                'action': 'Planifier audit mensuel'
            },
            {
                'title': '📚 Formation Utilisateurs',
                'desc': 'Sensibilisez les utilisateurs aux bonnes pratiques de sécurité informatique.',
                'priority': 'low',
                'action': 'Organiser formation'
            },
            {
                'title': '💾 Stratégie de Sauvegarde',
                'desc': 'Vérifiez régulièrement vos sauvegardes et testez les procédures de restauration.',
                'priority': 'medium',
                'action': 'Test de restauration'
            }
        ])

        for i, rec in enumerate(recommendations):
            priority_colors = {
                'critical': ('#dc3545', '#721c24'),
                'high': ('#fd7e14', '#fd7e14'),
                'medium': ('#ffc107', '#856404'),
                'low': ('#28a745', '#155724')
            }
            bg_color, text_color = priority_colors.get(rec['priority'], ('#17a2b8', '#0c5460'))

            priority_text = {
                'critical': '🚨 CRITIQUE',
                'high': '🔥 HAUTE',
                'medium': '⚠️ MOYENNE',
                'low': '✅ FAIBLE'
            }.get(rec['priority'], '📋 INFO')

            html += f"""
                    <div style="padding: 25px; background: linear-gradient(135deg, white 0%, #f8f9fa 100%); border-radius: 12px; border-left: 5px solid {bg_color}; box-shadow: 0 4px 8px rgba(0,0,0,0.1); transition: transform 0.2s ease;" onmouseover="this.style.transform='translateY(-3px)'" onmouseout="this.style.transform='translateY(0)'">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;">
                            <h4 style="margin: 0; color: #2c3e50; font-size: 1.1em;">{rec['title']}</h4>
                            <span style="background: {bg_color}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.75em; font-weight: 600;">{priority_text}</span>
                        </div>
                        <p style="color: #495057; line-height: 1.6; margin-bottom: 15px;">{rec['desc']}</p>
                        <div style="background: linear-gradient(135deg, {bg_color}15, {bg_color}25); padding: 10px; border-radius: 8px; color: {text_color}; font-weight: 500; font-size: 0.9em;">
                            📋 Action: {rec['action']}
                        </div>
                    </div>"""

        html += f"""
                </div>
            </div>

            <!-- Statistiques Détaillées -->
            <div class="section">
                <h2>📊 Statistiques Détaillées</h2>
                <div class="info-grid">
                    <div class="info-item" style="border-left-color: #28a745;">
                        <strong>✅ Logiciels Conformes:</strong><br>
                        {up_to_date_count} sur {installed_count} installés<br>
                        <small style="color: #6c757d;">({round((up_to_date_count/installed_count*100), 1) if installed_count > 0 else 0}% de conformité)</small>
                    </div>
                    <div class="info-item" style="border-left-color: #ffc107;">
                        <strong>⚠️ Mises à Jour Requises:</strong><br>
                        {outdated_count} logiciel(s)<br>
                        <small style="color: #6c757d;">Risque de vulnérabilités</small>
                    </div>
                    <div class="info-item" style="border-left-color: #dc3545;">
                        <strong>❌ Non Installés:</strong><br>
                        {missing_count} logiciel(s)<br>
                        <small style="color: #6c757d;">Fonctionnalités manquantes</small>
                    </div>
                    <div class="info-item" style="border-left-color: #17a2b8;">
                        <strong>🔒 Sécurité Globale:</strong><br>
                        Score: {stats['security_score']}/100<br>
                        <small style="color: #6c757d;">
                            {'🛡️ Excellent' if stats['security_score'] >= 90 else
                             '✅ Bon' if stats['security_score'] >= 80 else
                             '⚠️ Moyen' if stats['security_score'] >= 60 else
                             '🚨 Faible'}
                        </small>
                    </div>
                    <div class="info-item" style="border-left-color: #6f42c1;">
                        <strong>📈 Couverture Logicielle:</strong><br>
                        {installed_count}/{len(software_results)} logiciels<br>
                        <small style="color: #6c757d;">({round((installed_count/len(software_results)*100), 1)}% d'installation)</small>
                    </div>
                    <div class="info-item" style="border-left-color: #fd7e14;">
                        <strong>🛠️ Actions Prioritaires:</strong><br>
                        {len([r for r in recommendations if r['priority'] in ['critical', 'high']])} action(s)<br>
                        <small style="color: #6c757d;">Traitement urgent requis</small>
                    </div>
                </div>
            </div>

            <!-- Top 10 des Logiciels Critiques -->
            <div class="section">
                <h2>🎯 Top 10 - Logiciels Critiques à Mettre à Jour</h2>
                <div class="table-container">"""

        critical_software = [s for s in software_sorted if s['status'] == 'Obsolète' and
                           any(keyword in s['software'].lower() for keyword in
                               ['chrome', 'firefox', 'edge', 'java', 'python', 'windows defender',
                                'office', 'teams', 'zoom', 'adobe'])][:10]

        if critical_software:
            html += """
                    <table>
                        <thead>
                            <tr>
                                <th>Priorité</th>
                                <th>Logiciel Critique</th>
                                <th>Version Actuelle</th>
                                <th>Version Requise</th>
                                <th>Risque</th>
                            </tr>
                        </thead>
                        <tbody>"""

            for i, soft in enumerate(critical_software, 1):
                risk_level = {
                    1: ('🚨 CRITIQUE', 'status-error'),
                    2: ('🔥 TRÈS ÉLEVÉ', 'status-error'),
                    3: ('⚠️ ÉLEVÉ', 'status-warning')
                }.get(i, ('⚠️ MOYEN', 'status-warning'))

                html += f"""
                            <tr>
                                <td><strong>#{i}</strong></td>
                                <td><strong>{soft['software']}</strong></td>
                                <td><code style="background: #fff3cd; padding: 2px 6px; border-radius: 4px;">{soft['current_version']}</code></td>
                                <td><code style="background: #d4edda; padding: 2px 6px; border-radius: 4px;">{soft['required_version']}</code></td>
                                <td><span class="{risk_level[1]}">{risk_level[0]}</span></td>
                            </tr>"""

            html += """
                        </tbody>
                    </table>"""
        else:
            html += """
                    <div style="text-align: center; padding: 40px; color: #28a745;">
                        <h3>🎉 Excellent !</h3>
                        <p>Aucun logiciel critique n'est obsolète. Votre système est bien maintenu.</p>
                    </div>"""

        html += """
                </div>
            </div>
        </div>

        <div class="footer">
            <p><strong>🛡️ Rapport généré par HawKey Security Suite v2.1</strong></p>
            <p>📅 Date de génération: """ + datetime.datetime.now().strftime('%d/%m/%Y à %H:%M:%S') + f"""</p>
            <p>🔒 Audit local et logiciels consolidé - {len(software_results)} logiciels analysés</p>
            <p style="margin-top: 15px; font-size: 0.9em; opacity: 0.8;">
                ⚡ Scan optimisé | 🎯 Recommandations personnalisées | 📊 Analyse approfondie | 🔍 Recherche interactive
            </p>
            <div style="margin-top: 15px; padding: 15px; background: linear-gradient(135deg, #e3f2fd, #bbdefb); border-radius: 8px; border-left: 4px solid #2196f3;">
                <p style="margin: 0; color: #1565c0; font-weight: 500;">
                    💡 <strong>Conseil :</strong> Sauvegardez ce rapport et effectuez un nouvel audit dans 30 jours pour suivre l'évolution de votre sécurité.
                </p>
            </div>
        </div>
    </div>
</body>
</html>"""

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"✅ Rapport HTML généré: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Erreur génération rapport: {e}")
            return None


def main():
    """Point d'entrée principal"""
    try:
        auditor = HawKeyLocalAudit()
        success = auditor.run_full_audit()

        if success:
            print("\n✨ Audit terminé avec succès!")
        else:
            print("\n❌ Audit annulé")

    except KeyboardInterrupt:
        print("\n⚠️ Audit interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur critique: {e}")
    finally:
        input("\nAppuyez sur Entrée pour fermer...")


if __name__ == "__main__":
    main()