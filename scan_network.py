import socket 
import pyfiglet
import ipaddress
import psutil
import nmap
import os
from datetime import datetime
import subprocess

# Bannière
print(pyfiglet.figlet_format("Network Scanner"))

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

def scan_network(network_range, filename):
    """Effectue un scan réseau et génère un rapport HTML détaillé."""
    print("[INFO] Scan du réseau en cours...")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("""<html><head><title>Rapport Scan Réseau</title>
        <style>
            body {font-family: Arial, sans-serif; background: #f4f4f9; padding: 20px;}
            h1, h2 {color: #0044cc;}
            table {width: 100%; border-collapse: collapse;}
            th, td {border: 1px solid #ddd; padding: 10px;}
            th {background: #0044cc; color: white;}
            tr:nth-child(even) {background: #f9f9f9;}
            .cve {color: red;}
        </style></head><body>""")
        
        f.write(f"<h1>Scan réseau du {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h1>")
        f.write(f"<p>Plage réseau : {network_range}</p>")

        nm = nmap.PortScanner()
        nm.scan(hosts=str(network_range), arguments="-sn")
        active_hosts = nm.all_hosts()

        if active_hosts:
            for host in active_hosts:
                f.write(f"<h2>Résultats pour {host}</h2>")
                scan_result = nmap_scan_for_cve(host)
                cve_dict = parse_nmap_cve(scan_result) if scan_result else {}
                
                f.write("<table>")
                f.write("<tr><th>Port - Service (Version)</th><th>CVEs Détectées</th></tr>")
                
                for service, cves in cve_dict.items():
                    cve_list = "<br>".join(cves) if cves else "Aucune"
                    f.write(f"<tr><td>{service}</td><td class='cve'>{cve_list}</td></tr>")
                
                f.write("</table><br>")
        else:
            f.write("<p>Aucune machine active détectée.</p>")

        f.write("</body></html>")
    print("[INFO] Scan terminé. Rapport enregistré en HTML.")

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
        filename = f"C:\\Audit\\RapportCVE_{date_str}.html"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        scan_network(network_range, filename)
    else:
        print("[ERREUR] Aucune adresse IP IPv4 trouvée pour cette interface.")
