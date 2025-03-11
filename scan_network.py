import socket
import pyfiglet
import ipaddress
import psutil
import nmap
import os
from datetime import datetime
from tabulate import tabulate
import requests

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

def get_cve_from_version(service, version):
    """Interroge l'API pour obtenir les CVE pour un service et une version donnés."""
    url = f"https://cve.circl.lu/api/search/?service={service}&version={version}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        cve_list = data.get("matches", [])
        return cve_list
    return []

def scan_network(network_range, filename):
    """Effectue un scan réseau avec nmap pour détecter les machines actives, leurs ports ouverts et les versions des services."""
    nm = nmap.PortScanner()
    print("[INFO] Scan du réseau en cours...\n")

    # Scanner les hôtes actifs sur la plage réseau
    nm.scan(hosts=str(network_range), arguments="-sn")
    active_hosts = nm.all_hosts()

    # Ouvrir le fichier HTML pour y écrire les résultats
    with open(filename, "w", encoding="utf-8") as f:
        # Ajouter le style CSS pour améliorer l'apparence
        f.write("<html><head><title>Rapport de scan réseau - {}</title>".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        f.write("""
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                color: #333;
                padding: 20px;
            }
            h1, h2 {
                color: #0044cc;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                background-color: #fff;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            th, td {
                padding: 12px;
                text-align: left;
                border: 1px solid #ddd;
            }
            th {
                background-color: #0044cc;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            tr:hover {
                background-color: #e9f2ff;
            }
            .cve {
                color: red;
            }
        </style>
        </head><body>""")
        
        f.write(f"<h1>Scan réseau effectué le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h1>\n")
        f.write(f"<p>Plage réseau : {network_range}</p>\n")

        if active_hosts:
            for host in active_hosts:
                f.write(f"<h2>Nmap scan report for {host}</h2>\n")
                print(f"Nmap scan report for {host}")
                
                # Scanner les ports ouverts et les versions des services
                nm.scan(host, arguments="-p 1-65535 --open -sV")
                
                if "mac" in nm[host]["addresses"]:
                    mac_address = nm[host]["addresses"]["mac"]
                    f.write(f"<p>MAC Address: {mac_address}</p>\n")
                    print(f"MAC Address: {mac_address}")

                if "osmatch" in nm[host] and nm[host]["osmatch"]:
                    os_name = nm[host]["osmatch"][0]["name"]
                    f.write(f"<p>OS: {os_name}</p>\n")
                    print(f"OS: {os_name}")

                open_ports = nm[host].all_protocols()

                # Collecter les données pour créer un tableau
                table = []
                headers = ["PORT", "STATE", "SERVICE", "VERSION", "CVE"]

                if open_ports:
                    for proto in open_ports:
                        for port in nm[host][proto].keys():
                            service = nm[host][proto][port].get("name", "Unknown")
                            state = nm[host][proto][port]["state"]
                            version = nm[host][proto][port].get("version", "N/A")
                            product = nm[host][proto][port].get("product", "N/A")
                            
                            # Recherche des CVE pour la version du service
                            cve_list = get_cve_from_version(service, version)
                            cve_info = ", ".join([cve["id"] for cve in cve_list]) if cve_list else "No CVE found"

                            # Ajouter à la table
                            table.append([f"{port}/{proto}", state, service, f"{product} {version}", f"<span class='cve'>{cve_info}</span>"])
                else:
                    f.write("<p>No open ports found.</p>\n")
                    print("No open ports found.")

                # Écrire les résultats dans le fichier HTML sous forme de tableau
                f.write("<table>\n")
                f.write("<tr><th>PORT</th><th>STATE</th><th>SERVICE</th><th>VERSION</th><th>CVE</th></tr>\n")
                for row in table:
                    f.write("<tr>")
                    for col in row:
                        f.write(f"<td>{col}</td>")
                    f.write("</tr>\n")
                f.write("</table><br><br>\n")
                print(tabulate(table, headers, tablefmt="fancy_grid"))
        else:
            print("[INFO] Aucune machine active détectée.")
            f.write("<p>[INFO] Aucune machine active détectée.</p>\n")

        f.write("</body></html>")
    print("[INFO] Scan terminé. Rapport enregistré en HTML.")

if __name__ == "__main__":
    interfaces = list_network_interfaces()
    
    # Demander à l'utilisateur de choisir une interface
    choice = int(input("\n[INPUT] Choisissez une interface (numéro) : "))
    selected_interface = interfaces[choice]
    print(f"[INFO] Interface sélectionnée : {selected_interface}")
    
    # Obtenir les informations réseau de l'interface choisie
    ip_address, netmask = get_interface_info(selected_interface)
    if ip_address and netmask:
        print(f"[INFO] Adresse IP : {ip_address}")
        print(f"[INFO] Masque : {netmask}")
        
        # Calculer la plage réseau
        network_range = calculate_network_range(ip_address, netmask)
        print(f"[INFO] Plage réseau : {network_range}")
        
        # Créer le fichier de sortie avec la date du jour
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"C:\\Audit\\scan_{date_str}.html"
        
        # Vérifier que le dossier existe, sinon le créer
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Effectuer un scan réseau et enregistrer les résultats en HTML
        scan_network(network_range, filename)
    else:
        print("[ERREUR] Aucune adresse IP IPv4 trouvée pour cette interface.")
