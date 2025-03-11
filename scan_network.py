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
            return addr.address, addr.netmask
    return None, None

def calculate_network_range(ip_address, netmask):
    """Calcule la plage réseau en fonction de l'adresse IP et du masque."""
    return ipaddress.IPv4Network(f"{ip_address}/{netmask}", strict=False)

def scan_network(network_range, filename):
    """Effectue un scan réseau avec nmap pour détecter les machines actives, leurs ports ouverts et les versions des services."""
    nm = nmap.PortScanner()
    print("[INFO] Scan du réseau en cours...\n")

    # Scanner les hôtes actifs sur la plage réseau
    nm.scan(hosts=str(network_range), arguments="-sn")
    active_hosts = nm.all_hosts()

    with open(filename, "w") as f:
        f.write(f"Scan réseau effectué le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Plage réseau : {network_range}\n\n")

        if active_hosts:
            for host in active_hosts:
                f.write(f"Nmap scan report for {host}\n")
                print(f"Nmap scan report for {host}")
                
                # Scanner les ports ouverts et les versions des services
                nm.scan(host, arguments="-p 1-65535 --open -sV")
                
                if "mac" in nm[host]["addresses"]:
                    mac_address = nm[host]["addresses"]["mac"]
                    f.write(f"MAC Address: {mac_address}\n")
                    print(f"MAC Address: {mac_address}")

                if "osmatch" in nm[host] and nm[host]["osmatch"]:
                    os_name = nm[host]["osmatch"][0]["name"]
                    f.write(f"OS: {os_name}\n")
                    print(f"OS: {os_name}")

                open_ports = nm[host].all_protocols()

                if open_ports:
                    f.write("PORT\tSTATE\tSERVICE\tVERSION\n")
                    print("PORT\tSTATE\tSERVICE\tVERSION")

                    for proto in open_ports:
                        for port in nm[host][proto].keys():
                            service = nm[host][proto][port].get("name", "Unknown")
                            state = nm[host][proto][port]["state"]
                            version = nm[host][proto][port].get("version", "N/A")
                            product = nm[host][proto][port].get("product", "N/A")

                            f.write(f"{port}/{proto}\t{state}\t{service}\t{product} {version}\n")
                            print(f"{port}/{proto}\t{state}\t{service}\t{product} {version}")
                else:
                    f.write("No open ports found.\n")
                    print("No open ports found.")

                f.write("\n")
                print("\n")
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
        filename = f"C:\\Audit\\scan_{date_str}.txt"
        
        # Vérifier que le dossier existe, sinon le créer
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Effectuer un scan réseau et enregistrer les résultats
        scan_network(network_range, filename)
    else:
        print("[ERREUR] Aucune adresse IP IPv4 trouvée pour cette interface.")