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
    """Effectue un scan réseau avec nmap pour détecter les machines actives et leurs ports ouverts."""
    nm = nmap.PortScanner()
    print("[INFO] Scan du réseau en cours...")

    # Scanner toute la plage réseau avec un ping scan (-sn)
    nm.scan(hosts=str(network_range), arguments="-sn")

    active_hosts = nm.all_hosts()
    
    with open(filename, "w") as f:
        f.write(f"Scan réseau effectué le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Plage réseau : {network_range}\n")
        f.write("[INFO] Machines détectées :\n")

        if active_hosts:
            for host in active_hosts:
                f.write(f"Machine trouvée : {host}\n")
                print(f"[INFO] Machine trouvée : {host}")
                
                # Scanner les ports ouverts (1-65535)
                nm.scan(host, arguments="-p 1-65535 --open")
                open_ports = nm[host].all_tcp()

                if open_ports:
                    f.write(f"Ports ouverts sur {host} : {', '.join(map(str, open_ports))}\n")
                    print(f"[INFO] Ports ouverts sur {host} : {', '.join(map(str, open_ports))}")
                else:
                    f.write(f"Aucun port ouvert détecté sur {host}.\n")
                    print(f"[INFO] Aucun port ouvert détecté sur {host}.")
        else:
            print("[INFO] Aucune machine active détectée.")
            f.write("[INFO] Aucune machine active détectée.\n")

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
        filename = f"C:\\Users\\Iutuser\\Documents\\Projet PTUT Script\\Rapport Scan Réseau\\scan_{date_str}.txt"
        
        # Vérifier que le dossier existe, sinon le créer
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Effectuer un scan réseau et enregistrer les résultats
        scan_network(network_range, filename)
    else:
        print("[ERREUR] Aucune adresse IP IPv4 trouvée pour cette interface.")
