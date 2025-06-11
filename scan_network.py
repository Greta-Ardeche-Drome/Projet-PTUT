<<<<<<< HEAD
=======
# -*- coding: utf-8 -*-
>>>>>>> bb94804 (refactor: Modification des chemins pour la clé USB)
import socket
import pyfiglet
import ipaddress
import psutil
import nmap
import os
from datetime import datetime
import subprocess

# Bannière
print(pyfiglet.figlet_format("HawKey Scanner"))

def list_network_interfaces():
    """Liste toutes les interfaces réseau disponibles."""
    interfaces = psutil.net_if_addrs()
    print("[INFO] Interfaces réseau disponibles :")
    for idx, iface in enumerate(interfaces.keys()):
        print(f"{idx}. {iface}")
    return list(interfaces.keys())

def get_interface_info(interface):
    """Récupère les informations réseau d'une interface spécifique."""
    addresses = psutil.net_if_addrs().get(interface, [])
    for addr in addresses:
        if addr.family == socket.AF_INET:  # Adresse IPv4
            return addr.address, addr.netmask
    return None, None

def calculate_network_range(ip_address, netmask):
    """Calcule la plage réseau en fonction de l'adresse IP et du masque."""
    return ipaddress.IPv4Network(f"{ip_address}/{netmask}", strict=False)

def nmap_scan_for_cve(target_ip):
    """Effectue un scan nmap pour détecter les ports, services et CVE sur la cible."""
    print(f"[INFO] Scan des ports et services en cours sur {target_ip}...")
    nmap_path = r"C:\\Program Files (x86)\\Nmap\\nmap.exe"  # Modifier selon l'installation
    
    nmap_command = [
        nmap_path,
        "-T4", "-Pn", "-sV", "--script=vulners",
        "-p", "1-65535",
        target_ip
    ]
    try:
        result = subprocess.run(nmap_command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[ERREUR] Scan Nmap échoué: {result.stderr}")
            return ""
        return result.stdout
    except Exception as e:
        print(f"[ERREUR] Erreur lors du scan: {str(e)}")
        return ""

def parse_nmap_cve(scan_result):
    """Parse les résultats Nmap pour extraire les ports, services et CVE."""
    cve_dict = {}
    lines = scan_result.splitlines()
    current_service = ""
    
    for line in lines:
        if "/tcp" in line or "/udp" in line:
            parts = line.split()
            if len(parts) >= 3:
                port_service = parts[0]
                service_name = parts[2]
                version = " ".join(parts[3:]) if len(parts) > 3 else "Unknown"
                current_service = f"{port_service} - {service_name} ({version})"
                cve_dict[current_service] = []
        elif "CVE-" in line:
            if current_service:
                cve_dict[current_service].append(line.strip())
    return cve_dict

# ──────────────────────────────────────────────────────────────────────────────
#  Nouvelle fonction scan_network avec rapport HawKey-style
# ──────────────────────────────────────────────────────────────────────────────
def scan_network(network_range, filename):
    """Effectue un scan réseau et génère un rapport HTML détaillé HawKey-style."""
    print("[INFO] Scan du réseau en cours…")
    
    # 1) Phase découverte (ping sweep)
    nm = nmap.PortScanner()
    nm.scan(hosts=str(network_range), arguments="-sn")
    active_hosts = nm.all_hosts()
    
    # 2) Écriture du rapport
    with open(filename, "w", encoding="utf-8") as f:
        # ─── <head> + <header> + métriques ────────────────────────────────
        f.write(f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>HawKey – Rapport Scan Réseau</title>

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
      integrity="sha512-Dgv/25IfsVk1Y+xX1FCL4S8P9muj7p8Xr8YJVdlY2XkTYt/1qcRd4ek5smmJYfPbsAyf7jWqGtUGz05Wh06YxA==" crossorigin="anonymous" referrerpolicy="no-referrer" />

<style>
:root {{
  --primary:#0d47a1;
  --primary-dark:#002171;
  --success:#2e7d32;
  --danger:#c62828;
  --light:#f5f7ff;
  --text:#333;
}}
* {{box-sizing:border-box;margin:0;padding:0}}
body {{
  font-family:'Inter',sans-serif;
  background:var(--light);
  color:var(--text);
  padding:24px;
}}
header {{
  background:linear-gradient(135deg,var(--primary) 0%,var(--primary-dark) 100%);
  color:#fff;
  padding:32px 24px 40px;
  border-radius:16px;
  box-shadow:0 6px 12px rgba(0,0,0,.08);
  text-align:center;
}}
header i{{font-size:42px}}
header h1{{margin-top:8px;font-size:2.1rem;font-weight:700}}
header p{{opacity:.9;margin-top:4px}}

.metrics {{
  display:flex;flex-wrap:wrap;gap:16px;
  margin-top:-48px;
  justify-content:center;
}}
.metric-card {{
  flex:1 1 220px;
  background:#fff;
  padding:24px 16px;
  border-radius:16px;
  box-shadow:0 4px 10px rgba(0,0,0,.06);
  position:relative;
  overflow:hidden;
}}
.metric-card::before {{
  content:"";
  position:absolute;
  inset:0;
  border-top:4px solid transparent;
  border-image:linear-gradient(90deg,#ff6a00,#ee0979) 1;
}}
.metric-card h2{{font-size:2rem;font-weight:700}}
.metric-card span{{color:#555;font-size:.9rem}}

details.host {{
  margin-top:24px;
  background:#fff;
  border-radius:16px;
  box-shadow:0 4px 10px rgba(0,0,0,.05);
  overflow:hidden;
}}
details[open] summary{{border-bottom:1px solid #e3e7ff}}
summary {{
  padding:18px 20px;
  list-style:none;
  cursor:pointer;
  font-weight:600;
  display:flex;
  align-items:center;
  gap:10px;
  background:linear-gradient(90deg,#e3e7ff 0%,#f5f7ff 100%);
}}
summary i{{color:var(--primary)}}

table{{width:100%;border-collapse:collapse}}
th,td{{padding:12px 16px;text-align:left}}
th{{background:var(--primary);color:#fff}}
tr:nth-child(even){{background:#f0f3ff}}
.cve{{color:var(--danger);font-weight:600;font-size:.9rem}}
.no-cve{{color:var(--success);font-weight:600;font-size:.9rem}}

footer{{margin-top:40px;font-size:.8rem;text-align:center;opacity:.7}}
</style>
</head>
<body>

<header>
  <i class="fa-solid fa-shield-halved"></i>
  <h1>HawKey – Rapport Scan Réseau</h1>
  <p>Analyse détaillée de la posture réseau</p>
</header>

<section class="metrics">
  <div class="metric-card">
     <h2>{len(active_hosts)}</h2><span>Hôtes actifs</span>
  </div>
  <div class="metric-card">
     <h2>{network_range.num_addresses}</h2><span>Hôtes potentiels</span>
  </div>
  <div class="metric-card">
     <h2>{datetime.now().strftime('%d/%m/%Y')}</h2><span>Date du scan</span>
  </div>
</section>
""")
        # ─── Pour chaque hôte actif ───────────────────────────────────────
        if active_hosts:
            for host in active_hosts:
                f.write(f"""
<details class="host">
  <summary><i class="fa-solid fa-computer"></i>{host}</summary>
  <table>
    <tr><th>Port - Service (Version)</th><th>CVEs détectées</th></tr>
""")
                scan_result = nmap_scan_for_cve(host)
                cve_dict = parse_nmap_cve(scan_result) if scan_result else {}
                
                for service, cves in cve_dict.items():
                    cve_list = "<br>".join(cves) if cves else "<span class='no-cve'>Aucune</span>"
                    f.write(f"<tr><td>{service}</td><td class='cve'>{cve_list}</td></tr>")
                
                # Aucun service (ex. hôte up sans port ouvert découvert)
                if not cve_dict:
                    f.write("<tr><td colspan='2'><em>Aucun service détecté ou script Nmap indisponible.</em></td></tr>")
                
                f.write("</table>\n</details>\n")
        else:
            f.write("<p>Aucune machine active détectée.</p>")

        # ─── Footer & fermeture ───────────────────────────────────────────
        f.write("""
<footer>Généré par HawKey Scanner</footer>
</body></html>""")

    print("[INFO] Scan terminé. Rapport enregistré en HTML.")

# ──────────────────────────────────────────────────────────────────────────────
#  Main
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    interfaces = list_network_interfaces()
    choice = int(input("\n[INPUT] Choisissez une interface (numéro) : "))
    selected_interface = interfaces[choice]
    print(f"[INFO] Interface sélectionnée : {selected_interface}")
    
    ip_address, netmask = get_interface_info(selected_interface)
    if ip_address and netmask:
        print(f"[INFO] Adresse IP : {ip_address}")
        print(f"[INFO] Masque : {netmask}")
        network_range = calculate_network_range(ip_address, netmask)
        print(f"[INFO] Plage réseau : {network_range}")
        
        date_str = datetime.now().strftime("%Y-%m-%d")
<<<<<<< HEAD
        filename = f"C:/Users/antho/Documents/Projet-PTUT/RapportCVE_{date_str}.html"
=======
        filename = f"E:/HawKey/Rapport/RapportCVE_{date_str}.html"
>>>>>>> bb94804 (refactor: Modification des chemins pour la clé USB)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        scan_network(network_range, filename)
    else:
        print("[ERREUR] Aucune adresse IP IPv4 trouvée pour cette interface.")