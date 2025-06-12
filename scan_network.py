# -*- coding: utf-8 -*-
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

def scan_network(network_range, filename):
    """Effectue un scan réseau et génère un rapport HTML harmonisé avec le style HawKey."""
    print("[INFO] Scan du réseau en cours…")
    
    # 1) Phase découverte (ping sweep)
    nm = nmap.PortScanner()
    nm.scan(hosts=str(network_range), arguments="-sn")
    active_hosts = nm.all_hosts()
    
    # Calcul des statistiques
    total_hosts = network_range.num_addresses
    active_count = len(active_hosts)
    inactive_count = total_hosts - active_count
    coverage_percent = round((active_count / total_hosts * 100), 1) if total_hosts > 0 else 0
    
    # Compteurs pour les services/CVE
    total_services = 0
    total_cves = 0
    high_risk_hosts = 0
    
    # Pré-scan pour les statistiques
    host_data = {}
    for host in active_hosts:
        scan_result = nmap_scan_for_cve(host)
        cve_dict = parse_nmap_cve(scan_result) if scan_result else {}
        host_data[host] = cve_dict
        
        services_count = len(cve_dict)
        cves_count = sum(len(cves) for cves in cve_dict.values())
        total_services += services_count
        total_cves += cves_count
        
        if cves_count > 0:
            high_risk_hosts += 1
    
    # 2) Écriture du rapport avec le style harmonisé
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HawKey - Scan Réseau v2.1</title>
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
        
        .host-card {{
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: all 0.3s ease;
        }}
        .host-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        }}
        .host-header {{
            background: linear-gradient(135deg, #495057 0%, #6c757d 100%);
            color: white;
            padding: 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .host-header h3 {{
            margin: 0;
            font-size: 1.3em;
            font-weight: 600;
        }}
        .host-status {{
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .status-secure {{ 
            background: linear-gradient(135deg, #d4edda, #c3e6cb); 
            color: #155724; 
        }}
        .status-vulnerable {{ 
            background: linear-gradient(135deg, #f8d7da, #f5c6cb); 
            color: #721c24; 
        }}
        .status-unknown {{ 
            background: linear-gradient(135deg, #e2e3e5, #d1ecf1); 
            color: #0c5460; 
        }}
        
        .host-details {{
            display: none;
            padding: 0;
        }}
        .host-details.show {{
            display: block;
        }}
        
        .table-container {{
            background: white;
            overflow: hidden;
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
        }}
        
        .cve-list {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #f8d7da, #f5c6cb);
            padding: 8px 12px;
            border-radius: 6px;
            color: #721c24;
            font-size: 0.85em;
            font-weight: 600;
        }}
        .no-cve {{
            background: linear-gradient(135deg, #d4edda, #c3e6cb);
            color: #155724;
            padding: 8px 12px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.85em;
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
        
        .no-hosts {{
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 12px;
            border: 2px dashed #dee2e6;
        }}
        .no-hosts h3 {{
            color: #6c757d;
            font-size: 1.5em;
            margin-bottom: 10px;
        }}
        .no-hosts p {{
            color: #868e96;
            font-size: 1.1em;
        }}
        
        .critical-services {{
            background: linear-gradient(135deg, #fff3cd, #ffeaa7);
            border-left: 4px solid #ffc107;
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
        }}
        .critical-services h4 {{
            color: #856404;
            margin-bottom: 10px;
        }}
        
        @media (max-width: 768px) {{
            .summary-grid {{ grid-template-columns: 1fr; }}
            .info-grid {{ grid-template-columns: 1fr; }}
            .header h1 {{ font-size: 2em; }}
            .content {{ padding: 20px; }}
            .host-header {{ flex-direction: column; gap: 10px; }}
        }}
    </style>
    <script>
        function toggleHost(hostId) {{
            const details = document.getElementById('details-' + hostId);
            const arrow = document.getElementById('arrow-' + hostId);
            const isVisible = details.classList.contains('show');
            
            if (isVisible) {{
                details.classList.remove('show');
                arrow.textContent = '▼';
            }} else {{
                details.classList.add('show');
                arrow.textContent = '▲';
            }}
        }}
        
        function filterHosts(type) {{
            const hostCards = document.querySelectorAll('.host-card');
            const buttons = document.querySelectorAll('.filter-btn');
            
            buttons.forEach(btn => btn.classList.remove('active'));
            document.querySelector('.filter-' + type).classList.add('active');
            
            hostCards.forEach(card => {{
                const statusElement = card.querySelector('.host-status');
                const statusText = statusElement.textContent.toLowerCase();
                
                if (type === 'all') {{
                    card.style.display = 'block';
                }} else if (type === 'vulnerable' && statusText.includes('cve')) {{
                    card.style.display = 'block';
                }} else if (type === 'secure' && statusText.includes('sécurisé')) {{
                    card.style.display = 'block';
                }} else if (type === 'unknown' && statusText.includes('vérifier')) {{
                    card.style.display = 'block';
                }} else {{
                    card.style.display = 'none';
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
            <h1>🌐 HawKey - Scan Réseau v2.1</h1>
            <p>Analyse approfondie de l'infrastructure réseau et détection des vulnérabilités</p>
            <div style="margin-top: 15px; font-size: 0.9em; opacity: 0.8;">
                🔍 {active_count} hôte(s) actif(s) détecté(s) | 📊 Analyse CVE automatisée | ⚡ Scan Nmap avancé
            </div>
        </div>
        
        <div class="content">
            <!-- Résumé Exécutif -->
            <div class="summary-grid">
                <div class="summary-card {'success-card' if active_count > 0 else 'info-card'}">
                    <h3>{active_count}</h3>
                    <p>Hôtes Actifs</p>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {min(100, coverage_percent * 2)}%;">
                            {coverage_percent}%
                        </div>
                    </div>
                </div>
                <div class="summary-card {'danger-card' if high_risk_hosts > 5 else 'warning-card' if high_risk_hosts > 0 else 'success-card'}">
                    <h3>{high_risk_hosts}</h3>
                    <p>Hôtes Vulnérables</p>
                </div>
                <div class="summary-card {'danger-card' if total_cves > 10 else 'warning-card' if total_cves > 0 else 'success-card'}">
                    <h3>{total_cves}</h3>
                    <p>CVE Détectées</p>
                </div>
                <div class="summary-card info-card">
                    <h3>{total_services}</h3>
                    <p>Services Exposés</p>
                </div>
            </div>
            
            <!-- Informations du Scan -->
            <div class="section">
                <h2>📊 Informations du Scan</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <strong>🌐 Plage Réseau:</strong><br>{network_range}
                    </div>
                    <div class="info-item">
                        <strong>📅 Date du Scan:</strong><br>{datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}
                    </div>
                    <div class="info-item">
                        <strong>🎯 Hôtes Potentiels:</strong><br>{total_hosts} adresse(s) IP
                    </div>
                    <div class="info-item">
                        <strong>📈 Taux de Découverte:</strong><br>{coverage_percent}% du réseau
                    </div>
                    <div class="info-item">
                        <strong>🔍 Méthode de Scan:</strong><br>Nmap avec détection CVE
                    </div>
                    <div class="info-item">
                        <strong>⚡ Performance:</strong><br>Scan optimisé T4
                    </div>
                </div>
            </div>""")

        # Alertes critiques si CVE détectées
        if total_cves > 0:
            f.write(f"""
            <!-- Alerte Sécurité -->
            <div class="section">
                <div class="critical-services">
                    <h4>🚨 Alerte Sécurité Critique</h4>
                    <p><strong>{total_cves} vulnérabilité(s) CVE détectée(s)</strong> sur {high_risk_hosts} hôte(s). Action immédiate recommandée.</p>
                    <ul style="margin-top: 10px; padding-left: 20px;">""")
            
            critical_cves = []
            for host, cve_dict in host_data.items():
                cves_count = sum(len(cves) for cves in cve_dict.values())
                if cves_count > 0:
                    critical_cves.append(f"<li><strong>{host}</strong>: {cves_count} CVE détectée(s)</li>")
            
            for cve in critical_cves[:5]:  # Limite à 5 pour éviter de surcharger
                f.write(f"                        {cve}")
            
            if len(critical_cves) > 5:
                f.write(f"                        <li><em>... et {len(critical_cves) - 5} autre(s) hôte(s) vulnérable(s)</em></li>")
            
            f.write("""
                    </ul>
                </div>
            </div>""")

        f.write(f"""
            
            <!-- Filtres et Liste des Hôtes -->
            <div class="section">
                <h2>🖥️ Hôtes Détectés ({active_count})</h2>
                
                <div style="display: flex; gap: 10px; margin-bottom: 25px; flex-wrap: wrap; justify-content: center;">
                    <button class="filter-btn filter-all" onclick="filterHosts('all')" style="padding: 10px 20px; border: none; border-radius: 25px; cursor: pointer; font-weight: 600; background: linear-gradient(135deg, #007bff, #0056b3); color: white;">
                        Tous ({active_count})
                    </button>
                    <button class="filter-btn filter-vulnerable" onclick="filterHosts('vulnerable')" style="padding: 10px 20px; border: none; border-radius: 25px; cursor: pointer; font-weight: 600; background: linear-gradient(135deg, #dc3545, #c82333); color: white;">
                        🚨 Vulnérables ({high_risk_hosts})
                    </button>
                    <button class="filter-btn filter-secure" onclick="filterHosts('secure')" style="padding: 10px 20px; border: none; border-radius: 25px; cursor: pointer; font-weight: 600; background: linear-gradient(135deg, #28a745, #1e7e34); color: white;">
                        ✅ Sécurisés ({active_count - high_risk_hosts})
                    </button>
                    <button class="filter-btn filter-unknown" onclick="filterHosts('unknown')" style="padding: 10px 20px; border: none; border-radius: 25px; cursor: pointer; font-weight: 600; background: linear-gradient(135deg, #ffc107, #e0a800); color: #212529;">
                        ⚠️ À Vérifier
                    </button>
                </div>""")

        if active_hosts:
            for i, host in enumerate(active_hosts):
                cve_dict = host_data[host]
                services_count = len(cve_dict)
                cves_count = sum(len(cves) for cves in cve_dict.values())
                
                # Déterminer le statut de sécurité
                if cves_count > 0:
                    status_class = "status-vulnerable"
                    status_text = f"🚨 {cves_count} CVE"
                elif services_count > 0:
                    status_class = "status-unknown"
                    status_text = "⚠️ À Vérifier"
                else:
                    status_class = "status-secure"
                    status_text = "✅ Sécurisé"
                
                f.write(f"""
                <div class="host-card">
                    <div class="host-header" onclick="toggleHost('{i}')">
                        <h3>🖥️ {host}</h3>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span class="{status_class} host-status">{status_text}</span>
                            <span id="arrow-{i}" style="color: #dee2e6; font-size: 1.2em;">▼</span>
                        </div>
                    </div>
                    <div class="host-details" id="details-{i}">""")
                
                if cve_dict:
                    f.write("""
                        <div class="table-container">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Port - Service (Version)</th>
                                        <th>Vulnérabilités CVE</th>
                                        <th>Niveau de Risque</th>
                                    </tr>
                                </thead>
                                <tbody>""")
                    
                    for service, cves in cve_dict.items():
                        if cves:
                            cve_display = "<div class='cve-list'>" + "<br>".join(cves[:3])
                            if len(cves) > 3:
                                cve_display += f"<br><em>... et {len(cves) - 3} CVE supplémentaire(s)</em>"
                            cve_display += "</div>"
                            
                            # Niveau de risque basé sur le nombre de CVE
                            if len(cves) >= 5:
                                risk_level = "<span class='status-vulnerable'>🚨 CRITIQUE</span>"
                            elif len(cves) >= 2:
                                risk_level = "<span class='status-vulnerable'>🔥 ÉLEVÉ</span>"
                            else:
                                risk_level = "<span style='background: linear-gradient(135deg, #fff3cd, #ffeaa7); color: #856404; padding: 6px 12px; border-radius: 20px; font-weight: 600; font-size: 0.85em;'>⚠️ MOYEN</span>"
                        else:
                            cve_display = "<div class='no-cve'>✅ Aucune CVE détectée</div>"
                            risk_level = "<span class='status-secure'>✅ SÉCURISÉ</span>"
                        
                        f.write(f"""
                                    <tr>
                                        <td><strong>{service}</strong></td>
                                        <td>{cve_display}</td>
                                        <td>{risk_level}</td>
                                    </tr>""")
                    
                    f.write("""
                                </tbody>
                            </table>
                        </div>""")
                else:
                    f.write("""
                        <div style="padding: 30px; text-align: center; color: #6c757d;">
                            <h4>🔍 Analyse en cours...</h4>
                            <p>Aucun service détecté ou analyse Nmap en attente.</p>
                            <p style="margin-top: 10px; font-size: 0.9em;">L'hôte répond au ping mais aucun port ouvert n'a été détecté.</p>
                        </div>""")
                
                f.write("</div></div>")
        else:
            f.write("""
                <div class="no-hosts">
                    <h3>🔍 Aucun hôte actif détecté</h3>
                    <p>Le réseau semble vide ou les hôtes ne répondent pas au ping.</p>
                    <p style="margin-top: 15px; font-size: 0.9em; color: #adb5bd;">
                        💡 Conseil : Vérifiez la configuration réseau et les pare-feux
                    </p>
                </div>""")

        f.write("</div>")

        # Top 10 des services les plus critiques
        if total_cves > 0:
            f.write("""
            
            <!-- Top Services Critiques -->
            <div class="section">
                <h2>🎯 Services les Plus Critiques</h2>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Rang</th>
                                <th>Hôte</th>
                                <th>Service</th>
                                <th>CVE Count</th>
                                <th>Priorité</th>
                            </tr>
                        </thead>
                        <tbody>""")
            
            # Créer une liste des services critiques
            critical_services = []
            for host, cve_dict in host_data.items():
                for service, cves in cve_dict.items():
                    if cves:
                        critical_services.append({
                            'host': host,
                            'service': service,
                            'cve_count': len(cves),
                            'cves': cves
                        })
            
            # Trier par nombre de CVE décroissant
            critical_services.sort(key=lambda x: x['cve_count'], reverse=True)
            
            for i, service_data in enumerate(critical_services[:10], 1):
                priority_class = "status-vulnerable" if service_data['cve_count'] >= 3 else "status-warning" if service_data['cve_count'] >= 2 else "status-unknown"
                priority_text = "🚨 CRITIQUE" if service_data['cve_count'] >= 5 else "🔥 ÉLEVÉ" if service_data['cve_count'] >= 3 else "⚠️ MOYEN"
                
                f.write(f"""
                            <tr>
                                <td><strong>#{i}</strong></td>
                                <td>{service_data['host']}</td>
                                <td><code style="background: #f8f9fa; padding: 4px 8px; border-radius: 4px;">{service_data['service']}</code></td>
                                <td><span style="background: #f8d7da; color: #721c24; padding: 4px 8px; border-radius: 12px; font-weight: 600;">{service_data['cve_count']}</span></td>
                                <td><span class="{priority_class}">{priority_text}</span></td>
                            </tr>""")
            
            f.write("""
                        </tbody>
                    </table>
                </div>
            </div>""")

        # Recommandations de sécurité
        f.write(f"""
            
            <!-- Recommandations de Sécurité -->
            <div class="section">
                <h2>🎯 Recommandations de Sécurité</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px;">""")
        
        recommendations = []
        
        if total_cves > 10:
            recommendations.append({
                'title': '🚨 Nombreuses Vulnérabilités Détectées',
                'desc': f'{total_cves} CVE identifiées sur le réseau. Action immédiate requise pour éviter une compromission.',
                'priority': 'critical',
                'action': 'Corriger immédiatement'
            })
        elif total_cves > 0:
            recommendations.append({
                'title': '⚠️ Vulnérabilités à Traiter',
                'desc': f'{total_cves} CVE détectée(s). Planifier les corrections dans les plus brefs délais.',
                'priority': 'high',
                'action': 'Planifier les correctifs'
            })
        
        if high_risk_hosts > 3:
            recommendations.append({
                'title': '🔥 Multiples Hôtes à Risque',
                'desc': f'{high_risk_hosts} hôte(s) présente(nt) des vulnérabilités. Risque de propagation d\'attaque.',
                'priority': 'critical',
                'action': 'Isolation et correction urgente'
            })
        elif high_risk_hosts > 0:
            recommendations.append({
                'title': '🎯 Hôtes Vulnérables Identifiés',
                'desc': f'{high_risk_hosts} hôte(s) nécessite(nt) une attention particulière.',
                'priority': 'high',
                'action': 'Prioriser les corrections'
            })
        
        if total_services > 50:
            recommendations.append({
                'title': '📡 Surface d\'Attaque Étendue',
                'desc': f'{total_services} services exposés détectés. Réduire l\'exposition peut améliorer la sécurité.',
                'priority': 'medium',
                'action': 'Audit des services'
            })
        
        if active_count == 0:
            recommendations.append({
                'title': '🔍 Réseau Silencieux',
                'desc': 'Aucun hôte détecté. Vérifiez la configuration réseau ou les pare-feux.',
                'priority': 'medium',
                'action': 'Vérifier configuration'
            })
        
        recommendations.extend([
            {
                'title': '🔄 Surveillance Continue',
                'desc': 'Mettez en place une surveillance réseau continue pour détecter les nouvelles menaces.',
                'priority': 'medium',
                'action': 'Implémenter monitoring'
            },
            {
                'title': '🛡️ Segmentation Réseau',
                'desc': 'Séparez les services critiques des services moins sensibles pour limiter la propagation.',
                'priority': 'medium',
                'action': 'Réviser architecture'
            },
            {
                'title': '🔐 Durcissement des Services',
                'desc': 'Désactivez les services inutiles et mettez à jour les versions obsolètes.',
                'priority': 'high',
                'action': 'Hardening système'
            },
            {
                'title': '📋 Audit Régulier',
                'desc': 'Effectuez ce scan hebdomadairement pour maintenir la visibilité sur votre sécurité.',
                'priority': 'low',
                'action': 'Programmer scans'
            },
            {
                'title': '🚪 Gestion des Accès',
                'desc': 'Implémentez une authentification forte et des contrôles d\'accès granulaires.',
                'priority': 'medium',
                'action': 'Réviser IAM'
            },
            {
                'title': '📊 Corrélation avec Audit Local',
                'desc': 'Combinez ces résultats avec l\'audit local HawKey pour une vue d\'ensemble complète.',
                'priority': 'low',
                'action': 'Analyse croisée'
            }
        ])
        
        for rec in recommendations:
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
            
            f.write(f"""
                    <div style="padding: 25px; background: linear-gradient(135deg, white 0%, #f8f9fa 100%); border-radius: 12px; border-left: 5px solid {bg_color}; box-shadow: 0 4px 8px rgba(0,0,0,0.1); transition: transform 0.2s ease;" onmouseover="this.style.transform='translateY(-3px)'" onmouseout="this.style.transform='translateY(0)'">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;">
                            <h4 style="margin: 0; color: #2c3e50; font-size: 1.1em;">{rec['title']}</h4>
                            <span style="background: {bg_color}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.75em; font-weight: 600;">{priority_text}</span>
                        </div>
                        <p style="color: #495057; line-height: 1.6; margin-bottom: 15px;">{rec['desc']}</p>
                        <div style="background: linear-gradient(135deg, {bg_color}15, {bg_color}25); padding: 10px; border-radius: 8px; color: {text_color}; font-weight: 500; font-size: 0.9em;">
                            📋 Action: {rec['action']}
                        </div>
                    </div>""")
        
        f.write(f"""
                </div>
            </div>
            
            <!-- Statistiques Détaillées -->
            <div class="section">
                <h2>📊 Statistiques Détaillées</h2>
                <div class="info-grid">
                    <div class="info-item" style="border-left-color: #28a745;">
                        <strong>✅ Hôtes Sécurisés:</strong><br>
                        {active_count - high_risk_hosts} sur {active_count} actifs<br>
                        <small style="color: #6c757d;">({round(((active_count - high_risk_hosts)/active_count*100), 1) if active_count > 0 else 0}% du réseau actif)</small>
                    </div>
                    <div class="info-item" style="border-left-color: #dc3545;">
                        <strong>🚨 Hôtes Vulnérables:</strong><br>
                        {high_risk_hosts} hôte(s)<br>
                        <small style="color: #6c757d;">Nécessitent une attention immédiate</small>
                    </div>
                    <div class="info-item" style="border-left-color: #ffc107;">
                        <strong>📡 Services Exposés:</strong><br>
                        {total_services} service(s)<br>
                        <small style="color: #6c757d;">Surface d'attaque potentielle</small>
                    </div>
                    <div class="info-item" style="border-left-color: #17a2b8;">
                        <strong>🎯 Taux de Découverte:</strong><br>
                        {coverage_percent}% du réseau<br>
                        <small style="color: #6c757d;">{active_count}/{total_hosts} hôtes détectés</small>
                    </div>
                    <div class="info-item" style="border-left-color: #6f42c1;">
                        <strong>🔍 CVE Totales:</strong><br>
                        {total_cves} vulnérabilité(s)<br>
                        <small style="color: #6c757d;">
                            {'🛡️ Excellent' if total_cves == 0 else 
                             '⚠️ Attention' if total_cves <= 5 else 
                             '🚨 Critique' if total_cves > 10 else '⚠️ Modéré'}
                        </small>
                    </div>
                    <div class="info-item" style="border-left-color: #fd7e14;">
                        <strong>⏱️ Temps de Scan:</strong><br>
                        Scan en temps réel<br>
                        <small style="color: #6c757d;">Nmap T4 optimisé</small>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>🌐 Rapport généré par HawKey Network Scanner v2.1</strong></p>
            <p>📅 Date de génération: """ + datetime.now().strftime('%d/%m/%Y à %H:%M:%S') + f"""</p>
            <p>🔍 Scan réseau complet - {active_count} hôte(s) analysé(s) | {total_services} service(s) détecté(s) | {total_cves} CVE identifiée(s)</p>
            <p style="margin-top: 15px; font-size: 0.9em; opacity: 0.8;">
                ⚡ Scan Nmap optimisé | 🎯 Détection CVE automatisée | 🔍 Analyse approfondie | 📊 Recommandations personnalisées
            </p>
            <div style="margin-top: 15px; padding: 15px; background: linear-gradient(135deg, #e3f2fd, #bbdefb); border-radius: 8px; border-left: 4px solid #2196f3;">
                <p style="margin: 0; color: #1565c0; font-weight: 500;">
                    💡 <strong>Conseil :</strong> Combinez ce scan avec l'audit local HawKey pour une vue complète de votre posture de sécurité.
                </p>
            </div>
        </div>
    </div>
</body>
</html>""")

    print("[INFO] Scan terminé. Rapport HTML harmonisé enregistré.")

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
        filename = f"E:/HawKey/Rapport/RapportCVE_{date_str}.html"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        scan_network(network_range, filename)
    else:
        print("[ERREUR] Aucune adresse IP IPv4 trouvée pour cette interface.")