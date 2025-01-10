import socket
import pyfiglet
import ipaddress
import psutil
import nmap
import os
from datetime import datetime

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
            ip_address = addr.address
            netmask = addr.netmask
            return ip_address, netmask
    return None, None

def calculate_network_range(ip_address, netmask):
    """Calcule la plage réseau en fonction de l'adresse IP et du masque."""
    network = ipaddress.IPv4Network(f"{ip_address}/{netmask}", strict=False)
    return network

def scan_network(network_range, filename):
    """Effectue un scan réseau pour détecter les machines actives et affiche la progression."""
    nm = nmap.PortScanner()
    print("[INFO] Scan du réseau en cours...")
    
    # Ouvrir le fichier de sortie
    with open(filename, "w") as f:
        f.write(f"Scan réseau effectué le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Plage réseau : {network_range}\n")
        f.write("[INFO] Machines détectées :\n")
        
        # Scanner chaque hôte dans la plage
        for ip in network_range.hosts():
            print(f"[INFO] Scan en cours pour {ip}...")
            nm.scan(str(ip), '1-65535')  # Scanner tous les ports de 1 à 65535
            if nm.all_hosts():
                for host in nm.all_hosts():
                    f.write(f"Machine trouvée : {host}\n")
                    print(f"[INFO] Machine trouvée : {host}")
            else:
                print(f"[INFO] Aucune machine trouvée pour {ip}")
    print("[INFO] Scan terminé. Résultats enregistrés.")

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
        filename = f"C:\\Users\\Iutuser\\Documents\\Projet PTUT Script\\scan_{date_str}.txt"
        
        # Effectuer un scan réseau et enregistrer les résultats
        scan_network(network_range, filename)
    else:
        print("[ERREUR] Aucune adresse IP IPv4 trouvée pour cette interface.")
