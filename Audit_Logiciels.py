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

# Liste des logiciels requis avec leurs versions minimales (Mises à jour Mai 2025)
required_software = {
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
    'Tor Browser': '13.5',
    'Brave Browser': '1.66.118',
    'DuckDuckGo Browser': '1.80.0',
    'Waterfox': '6.0.13',
    'LibreWolf': '126.0',

    # Outils de Test et Qualité
    'Selenium WebDriver': '4.21.0',
    'JMeter': '5.6.3',
    'LoadRunner': '2024',
    'Burp Suite': '2024.5.2',
    'OWASP ZAP': '2.15.0'
}

# Définition des alternatives pour les noms de logiciels (pour la recherche flexible)
software_aliases = {
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
    'Spotify': ['Spotify Music'],
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
    'Thunderbird': ['Mozilla Thunderbird'],
    'Outlook': ['Microsoft Outlook'],
    'OneNote': ['Microsoft OneNote'],
    'Adobe Photoshop': ['Photoshop'],
    'Adobe Illustrator': ['Illustrator'],
    'Blender': ['Blender 3D'],
    'Krita': ['Krita Digital Painting'],
    'LibreOffice': ['LibreOffice Writer', 'LibreOffice Calc'],
    'OpenOffice': ['Apache OpenOffice'],
    'IrfanView': ['IrfanView Graphic Viewer'],
    'SumatraPDF': ['SumatraPDF Reader'],
    'Foxit PDF Reader': ['Foxit Reader'],
    'K-Lite Codec Pack': ['K-Lite Codecs'],
    'Advanced IP Scanner': ['Advanced IP Scanner Portable'],
    'Angry IP Scanner': ['ipscan'],
    'MySQL Workbench': ['MySQL'],
    'DBeaver': ['DBeaver Community'],
    'PostgreSQL': ['PostgreSQL Database Server'],
    'HeidiSQL': ['HeidiSQL MySQL Client'],
    'Process Explorer': ['Process Explorer Sysinternals'],
    'CPU-Z': ['CPUID CPU-Z'],
    'GPU-Z': ['TechPowerUp GPU-Z'],
    'HWiNFO': ['HWiNFO64'],
    'Crystal Disk Info': ['CrystalDiskInfo'],
    'Speccy': ['Piriform Speccy'],
    'Revo Uninstaller': ['Revo Uninstaller Pro'],
    'Glary Utilities': ['Glary Utilities Pro'],
    'Wise Care 365': ['Wise Care'],
    'Advanced SystemCare': ['IObit Advanced SystemCare'],
    'Macrium Reflect': ['Macrium Reflect Free'],
    'AOMEI Backupper': ['AOMEI Backupper Standard'],
    'EaseUS Todo Backup': ['EaseUS Todo'],
    'UltraVNC': ['UltraVNC Server', 'UltraVNC Viewer'],
    'TightVNC': ['TightVNC Server', 'TightVNC Viewer'],
    'OpenVPN': ['OpenVPN Connect'],
    'WireGuard': ['WireGuard VPN'],
    'Tor Browser': ['Tor'],
    'Brave Browser': ['Brave'],
    'DuckDuckGo Browser': ['DuckDuckGo'],
    'Waterfox': ['Waterfox Current'],
    'LibreWolf': ['LibreWolf Browser']
}


def is_admin():
    """
    Vérifie si le script est exécuté avec des privilèges d'administrateur.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False


def get_installed_software():
    """
    Récupère la liste des logiciels installés sur le système.
    """
    software = []

    # Chemins de registre à vérifier
    reg_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall")
    ]

    # Parcours des clés de registre
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
                    except (WindowsError, ValueError, TypeError):
                        pass
                    finally:
                        winreg.CloseKey(subkey)
                except WindowsError:
                    pass

            winreg.CloseKey(reg_key)
        except WindowsError:
            print(f"Erreur lors de l'accès au registre: {reg_path}")

    # Recherche des applications Windows Store (pour Windows 10/11)
    try:
        result = subprocess.run(
            ["powershell", "-Command", "Get-AppxPackage | Select-Object Name, Version | ConvertTo-Json"],
            capture_output=True, text=True, encoding='utf-8'
        )

        if result.returncode == 0:
            appx_data = json.loads(result.stdout)

            # Si un seul package est retourné, il n'est pas dans un tableau
            if isinstance(appx_data, dict):
                appx_data = [appx_data]

            for package in appx_data:
                if package.get('Name') and package.get('Version'):
                    software.append({
                        'DisplayName': package['Name'],
                        'DisplayVersion': package['Version']
                    })
    except (subprocess.SubprocessError, json.JSONDecodeError) as e:
        print(f"Erreur lors de la recherche des applications Store: {e}")

    return software


def compare_software_versions(installed_version, required_version):
    """
    Compare deux numéros de version.
    Retourne True si la version installée est supérieure ou égale à la version requise.
    """
    try:
        # Nettoyage des versions
        installed_clean = ''.join([c for c in installed_version if c.isdigit() or c == '.'])
        required_clean = ''.join([c for c in required_version if c.isdigit() or c == '.'])

        # Gestion de versions vides ou invalides
        if not installed_clean or not required_clean:
            return False

        # Division en segments
        installed_parts = [int(p) for p in installed_clean.split('.') if p]
        required_parts = [int(p) for p in required_clean.split('.') if p]

        # Comparaison par segment
        for i in range(max(len(installed_parts), len(required_parts))):
            installed_segment = installed_parts[i] if i < len(installed_parts) else 0
            required_segment = required_parts[i] if i < len(required_parts) else 0

            if installed_segment > required_segment:
                return True
            elif installed_segment < required_segment:
                return False

        # Si tous les segments sont égaux
        return True

    except Exception as e:
        print(f"Erreur lors de la comparaison des versions: '{installed_version}' avec '{required_version}'. Erreur: {e}")
        return False


def find_software_match(installed_software_list, software_name):
    """
    Recherche un logiciel dans la liste des logiciels installés.
    """
    # Recherche directe par nom exact
    matches = [s for s in installed_software_list if s['DisplayName'] == software_name]

    # Recherche avec une correspondance partielle (plus flexible)
    if not matches:
        matches = [s for s in installed_software_list 
                  if software_name.lower() in s['DisplayName'].lower() 
                  or s['DisplayName'].lower() in software_name.lower()]

    # Recherche avec des alias connus
    if not matches and software_name in software_aliases:
        for alias in software_aliases[software_name]:
            alias_matches = [s for s in installed_software_list 
                           if alias.lower() in s['DisplayName'].lower() 
                           or s['DisplayName'].lower() in alias.lower()]
            if alias_matches:
                matches = alias_matches
                break

    # Retourne la version la plus récente si plusieurs correspondances
    if matches and len(matches) > 1:
        try:
            # Trier par version (décroissant)
            def get_version_key(item):
                try:
                    version_str = ''.join([c for c in item['DisplayVersion'] if c.isdigit() or c == '.'])
                    parts = version_str.split('.')
                    parts = [int(p) for p in parts if p]
                    # Padding avec des zéros pour assurer une bonne comparaison
                    while len(parts) < 4:
                        parts.append(0)
                    return parts
                except:
                    return [0, 0, 0, 0]

            matches.sort(key=get_version_key, reverse=True)
            return matches[0]
        except Exception as e:
            print(f"Erreur lors du tri des versions pour {software_name}: {e}")
            return matches[0]

    return matches[0] if matches else None


def get_software_audit():
    """
    Effectue l'audit des logiciels installés.
    """
    results = []
    installed_software = get_installed_software()

    print("Analyse des logiciels en cours...")
    print(f"Total de logiciels à vérifier: {len(required_software)}")

    total = len(required_software)
    progress = 0

    for software, required_version in required_software.items():
        progress += 1
        percentage = round((progress / total) * 100)
        sys.stdout.write(f"\rProgression: {percentage}% - Vérification de {software}")
        sys.stdout.flush()

        installed = find_software_match(installed_software, software)

        if installed:
            version_conforme = compare_software_versions(installed['DisplayVersion'], required_version)

            results.append({
                'Logiciel': software,
                'Installation': True,
                'Version_Installee': installed['DisplayVersion'],
                'Version_Minimale': required_version,
                'Version_Conforme': version_conforme
            })
        else:
            # Logiciel non installé
            results.append({
                'Logiciel': software,
                'Installation': False,
                'Version_Installee': 'Non installé',
                'Version_Minimale': required_version,
                'Version_Conforme': False
            })

    print("\nAnalyse terminée!")
    return results


def export_html_report(audit_results, output_path):
    """
    Exporte les résultats de l'audit au format HTML avec design moderne.
    """
    # Comptage des logiciels
    installed_results = [r for r in audit_results if r['Installation']]
    conformes = len([r for r in installed_results if r['Version_Conforme']])
    non_conformes = len([r for r in installed_results if not r['Version_Conforme']])
    non_installes = len([r for r in audit_results if not r['Installation']])
    total_installed = len(installed_results)
    total_all = len(audit_results)

    # En-tête HTML avec design moderne
    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HawKey - Rapport d'Audit des Logiciels</title>
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
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ font-size: 1.2em; opacity: 0.9; }}
        .content {{ padding: 30px; }}
        .summary-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px; 
        }}
        .summary-card {{ 
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
            padding: 20px; 
            border-radius: 10px; 
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        .summary-card:hover {{ transform: translateY(-5px); }}
        .summary-card h3 {{ color: #2c3e50; margin-bottom: 10px; font-size: 2em; }}
        .summary-card p {{ color: #495057; font-weight: 500; }}
        .success-card {{ border-left: 4px solid #28a745; }}
        .warning-card {{ border-left: 4px solid #ffc107; }}
        .danger-card {{ border-left: 4px solid #dc3545; }}
        .info-card {{ border-left: 4px solid #17a2b8; }}
        .filters {{ 
            margin-bottom: 20px; 
            display: flex; 
            gap: 10px; 
            flex-wrap: wrap;
        }}
        .filter-btn {{ 
            padding: 8px 16px; 
            border: none; 
            border-radius: 20px; 
            cursor: pointer; 
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        .filter-btn.active {{ transform: scale(1.05); }}
        .filter-all {{ background: #007bff; color: white; }}
        .filter-success {{ background: #28a745; color: white; }}
        .filter-warning {{ background: #ffc107; color: black; }}
        .filter-danger {{ background: #dc3545; color: white; }}
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
            padding: 15px; 
            text-align: left;
            font-weight: 600;
        }}
        td {{ 
            padding: 12px 15px; 
            border-bottom: 1px solid #dee2e6; 
        }}
        tr:hover {{ background-color: #f8f9fa; }}
        .status-badge {{ 
            padding: 4px 12px; 
            border-radius: 20px; 
            font-size: 0.85em; 
            font-weight: bold; 
            text-transform: uppercase;
        }}
        .status-conforme {{ background: #d4edda; color: #155724; }}
        .status-obsolete {{ background: #fff3cd; color: #856404; }}
        .status-missing {{ background: #f8d7da; color: #721c24; }}
        .version-cell {{ font-family: 'Courier New', monospace; }}
        .footer {{ 
            background: #f8f9fa; 
            padding: 20px; 
            text-align: center; 
            color: #6c757d; 
            border-top: 1px solid #dee2e6;
        }}
        @media (max-width: 768px) {{
            .summary-grid {{ grid-template-columns: 1fr; }}
            .filters {{ justify-content: center; }}
            table {{ font-size: 14px; }}
            .header h1 {{ font-size: 2em; }}
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
                }} else if (status === 'danger' && statusCell.includes('installé')) {{
                    row.style.display = '';
                }} else {{
                    row.style.display = 'none';
                }}
            }});
        }}
        
        window.onload = function() {{
            document.querySelector('.filter-all').classList.add('active');
        }}
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 HawKey - Audit des Logiciels</h1>
            <p>Analyse complète des logiciels installés et de leur conformité</p>
        </div>
        
        <div class="content">
            <div class="summary-grid">
                <div class="summary-card success-card">
                    <h3>{conformes}</h3>
                    <p>Logiciels Conformes</p>
                </div>
                <div class="summary-card warning-card">
                    <h3>{non_conformes}</h3>
                    <p>Versions Obsolètes</p>
                </div>
                <div class="summary-card danger-card">
                    <h3>{non_installes}</h3>
                    <p>Non Installés</p>
                </div>
                <div class="summary-card info-card">
                    <h3>{total_installed}/{total_all}</h3>
                    <p>Logiciels Installés</p>
                </div>
            </div>

            <div style="background: #e7f3ff; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h3>📊 Résumé de l'Audit</h3>
                <p><strong>Date:</strong> {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                <p><strong>Ordinateur:</strong> {platform.node()}</p>
                <p><strong>Utilisateur:</strong> {os.getenv('USERNAME')}</p>
                <p><strong>Taux de conformité:</strong> {round((conformes / total_installed * 100), 1) if total_installed > 0 else 0}% des logiciels installés</p>
            </div>

            <div class="filters">
                <button class="filter-btn filter-all" onclick="filterTable('all')">Tous ({total_all})</button>
                <button class="filter-btn filter-success" onclick="filterTable('success')">Conformes ({conformes})</button>
                <button class="filter-btn filter-warning" onclick="filterTable('warning')">Obsolètes ({non_conformes})</button>
                <button class="filter-btn filter-danger" onclick="filterTable('danger')">Non Installés ({non_installes})</button>
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
                    <tbody>
"""

    # Ajout des lignes pour chaque logiciel
    for result in sorted(audit_results, key=lambda x: (not x['Installation'], not x['Version_Conforme'] if x['Installation'] else False, x['Logiciel'])):
        if not result['Installation']:
            status_class = "status-missing"
            status_text = "Non Installé"
            action = "Installation recommandée"
        elif result['Version_Conforme']:
            status_class = "status-conforme"
            status_text = "Conforme"
            action = "Aucune action requise"
        else:
            status_class = "status-obsolete"
            status_text = "Version Obsolète"
            action = "Mise à jour requise"

        html_content += f"""                        <tr>
                            <td><strong>{result['Logiciel']}</strong></td>
                            <td><span class="status-badge {status_class}">{status_text}</span></td>
                            <td class="version-cell">{result['Version_Installee']}</td>
                            <td class="version-cell">{result['Version_Minimale']}</td>
                            <td>{action}</td>
                        </tr>
"""

    # Pied de page HTML
    html_content += f"""                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>Rapport généré automatiquement par HawKey Security Suite</strong></p>
            <p>Date de génération: {datetime.datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</p>
            <p>Versions des logiciels mises à jour en Mai 2025</p>
        </div>
    </div>
</body>
</html>
"""

    # Écriture du fichier HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def export_csv_report(audit_results, output_path):
    """
    Exporte les résultats de l'audit au format CSV.
    """
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Logiciel', 'Installation', 'Version_Installee', 'Version_Minimale', 'Version_Conforme', 'Action_Recommandee']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for result in audit_results:
            if not result['Installation']:
                action = "Installation recommandée"
            elif result['Version_Conforme']:
                action = "Aucune action requise"
            else:
                action = "Mise à jour requise"
                
            writer.writerow({
                'Logiciel': result['Logiciel'],
                'Installation': 'Oui' if result['Installation'] else 'Non',
                'Version_Installee': result['Version_Installee'],
                'Version_Minimale': result['Version_Minimale'],
                'Version_Conforme': 'Oui' if result['Version_Conforme'] else 'Non',
                'Action_Recommandee': action
            })


def export_json_report(audit_results, output_path):
    """
    Exporte les résultats de l'audit au format JSON.
    """
    report_data = {
        'metadata': {
            'date_audit': datetime.datetime.now().isoformat(),
            'ordinateur': platform.node(),
            'utilisateur': os.getenv('USERNAME'),
            'version_script': '2.0',
            'total_logiciels': len(audit_results),
            'logiciels_installes': len([r for r in audit_results if r['Installation']]),
            'logiciels_conformes': len([r for r in audit_results if r['Installation'] and r['Version_Conforme']]),
            'logiciels_obsoletes': len([r for r in audit_results if r['Installation'] and not r['Version_Conforme']]),
            'logiciels_non_installes': len([r for r in audit_results if not r['Installation']])
        },
        'resultats': audit_results
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)


def ensure_report_folder(folder):
    """
    S'assure que le dossier de rapports existe, le crée si nécessaire.
    """
    try:
        os.makedirs(folder, exist_ok=True)
        print(f"Dossier de rapports: {folder}")
        return True
    except Exception as e:
        print(f"Impossible de créer le dossier de rapports: {e}")
        return False


def start_software_audit(output_folder="C:/Temp/Audits", generate_html=True, generate_csv=True, generate_json=False):
    """
    Fonction principale pour lancer l'audit des logiciels.
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    computer_name = platform.node().lower()

    # Vérification des droits d'administration
    if not is_admin():
        print("⚠️  Ce script nécessite des droits d'administration pour accéder à toutes les informations d'installation.")
        confirmation = input("Voulez-vous continuer quand même ? (O/N): ")
        if confirmation.upper() != "O":
            print("Opération annulée.")
            return

    # Création du dossier de rapports
    if not ensure_report_folder(output_folder):
        return

    # Affichage de l'en-tête moderne
    print("\n" + "="*60)
    print("🔍 HAWKEY - AUDIT DES LOGICIELS v2.0")
    print("="*60)
    print(f"📅 Date: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"💻 Ordinateur: {platform.node()}")
    print(f"👤 Utilisateur: {os.getenv('USERNAME')}")
    print(f"📁 Rapport: {output_folder}")
    print("="*60)

    # Exécution de l'audit
    start_time = time.time()
    audit_results = get_software_audit()
    elapsed_time = time.time() - start_time

    # Calcul des statistiques
    installed_results = [r for r in audit_results if r['Installation']]
    conformes = len([r for r in installed_results if r['Version_Conforme']])
    non_conformes = len([r for r in installed_results if not r['Version_Conforme']])
    non_installes = len([r for r in audit_results if not r['Installation']])
    total_installed = len(installed_results)
    total_all = len(audit_results)

    # Affichage des résultats
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DE L'AUDIT")
    print("="*60)
    print(f"🔍 Logiciels vérifiés: {total_all}")
    print(f"✅ Logiciels installés: {total_installed}")
    print(f"✅ Logiciels conformes: {conformes} ({round((conformes / total_installed * 100), 1)}% des installés)" if total_installed > 0 else "✅ Logiciels conformes: 0")
    print(f"⚠️  Versions obsolètes: {non_conformes}")
    print(f"❌ Non installés: {non_installes}")
    print(f"⏱️  Durée de l'audit: {elapsed_time:.2f} secondes")
    print("="*60)

    # Affichage des logiciels critiques obsolètes
    critical_obsolete = [r for r in audit_results 
                        if r['Installation'] and not r['Version_Conforme'] 
                        and any(keyword in r['Logiciel'].lower() 
                               for keyword in ['chrome', 'firefox', 'edge', 'java', 'python', 'windows defender'])]
    
    if critical_obsolete:
        print("\n⚠️  LOGICIELS CRITIQUES OBSOLÈTES:")
        for software in critical_obsolete:
            print(f"   • {software['Logiciel']}: {software['Version_Installee']} → {software['Version_Minimale']}")

    # Création du rapport texte détaillé
    txt_path = os.path.join(output_folder, f"audit_logiciels_{computer_name}_{timestamp}.txt")

    # Génération du contenu du rapport texte
    report = f"""HAWKEY - RAPPORT D'AUDIT DES LOGICIELS v2.0
{'='*50}
Date: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Ordinateur: {platform.node()}
Utilisateur: {os.getenv('USERNAME')}
Durée de l'audit: {elapsed_time:.2f} secondes

RÉSUMÉ EXÉCUTIF
{'='*50}
Logiciels vérifiés: {total_all}
Logiciels installés: {total_installed}
Logiciels conformes: {conformes} ({round((conformes / total_installed * 100), 1)}% des installés)
Versions obsolètes: {non_conformes}
Non installés: {non_installes}

NIVEAU DE SÉCURITÉ: {'ÉLEVÉ' if conformes/total_installed > 0.8 else 'MOYEN' if conformes/total_installed > 0.6 else 'FAIBLE'} 
Taux de conformité: {round((conformes / total_installed * 100), 1)}%

DÉTAILS PAR LOGICIEL
{'='*50}
"""

    # Grouper par statut
    conformes_list = [r for r in audit_results if r['Installation'] and r['Version_Conforme']]
    obsoletes_list = [r for r in audit_results if r['Installation'] and not r['Version_Conforme']]
    missing_list = [r for r in audit_results if not r['Installation']]

    if conformes_list:
        report += f"\n✅ LOGICIELS CONFORMES ({len(conformes_list)}):\n"
        for result in sorted(conformes_list, key=lambda x: x['Logiciel']):
            report += f"   • {result['Logiciel']}: {result['Version_Installee']}\n"

    if obsoletes_list:
        report += f"\n⚠️  VERSIONS OBSOLÈTES ({len(obsoletes_list)}):\n"
        for result in sorted(obsoletes_list, key=lambda x: x['Logiciel']):
            report += f"   • {result['Logiciel']}: {result['Version_Installee']} → {result['Version_Minimale']} (MISE À JOUR REQUISE)\n"

    if missing_list:
        report += f"\n❌ LOGICIELS NON INSTALLÉS ({len(missing_list)}):\n"
        for result in sorted(missing_list, key=lambda x: x['Logiciel']):
            report += f"   • {result['Logiciel']}: Version minimale {result['Version_Minimale']}\n"

    report += f"\n{'='*50}\nRapport généré automatiquement par HawKey Security Suite v2.0\n"
    report += f"Date de génération: {datetime.datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n"
    report += f"Versions mises à jour: Mai 2025\n"

    # Sauvegarde du rapport texte
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n📄 Rapport texte créé: {txt_path}")

    # Génération des rapports dans différents formats
    if generate_html:
        html_path = os.path.join(output_folder, f"audit_logiciels_{computer_name}_{timestamp}.html")
        export_html_report(audit_results, html_path)
        print(f"🌐 Rapport HTML créé: {html_path}")

    if generate_csv:
        csv_path = os.path.join(output_folder, f"audit_logiciels_{computer_name}_{timestamp}.csv")
        export_csv_report(audit_results, csv_path)
        print(f"📊 Rapport CSV créé: {csv_path}")

    if generate_json:
        json_path = os.path.join(output_folder, f"audit_logiciels_{computer_name}_{timestamp}.json")
        export_json_report(audit_results, json_path)
        print(f"📋 Rapport JSON créé: {json_path}")

    print(f"\n🎉 Audit terminé avec succès!")
    print(f"📁 Tous les rapports sont disponibles dans: {output_folder}")
    
    return audit_results


# Point d'entrée principal
if __name__ == "__main__":
    try:
        start_software_audit(generate_html=True, generate_csv=True, generate_json=True)
        print("\n✨ Appuyez sur Entrée pour fermer...")
        input()
    except KeyboardInterrupt:
        print("\n⚠️  Audit interrompu par l'utilisateur.")
    except Exception as e:
        print(f"\n❌ Erreur critique: {e}")
        print("📞 Contactez le support technique si le problème persiste.")
        input("Appuyez sur Entrée pour fermer...")