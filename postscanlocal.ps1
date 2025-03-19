# Définition des dossiers critiques à vérifier
$criticalFolders = @(
    "C:\Windows",
    "C:\Windows\System32", 
    "C:\Program Files",
    "C:\Program Files (x86)", 
    "C:\Users",
    "C:\Windows\System32\Config", 
    "C:\Windows\Temp"
)

# Ajout d'une boîte de dialogue pour nommer le dossier de rapport
Add-Type -AssemblyName Microsoft.VisualBasic
$dossierNom = [Microsoft.VisualBasic.Interaction]::InputBox("Quel nom voulez-vous donner au dossier de rapport ?", "Scan Permissions", "")

if ($dossierNom) {
    # Chemin de base pour les rapports
    $basePath = "C:\Users\Iutuser\Documents\Projet PTUT Script"
    $dossierChemin = Join-Path $basePath $dossierNom
    
    # Création du dossier si inexistant
    if (!(Test-Path $dossierChemin)) {
        New-Item -Type Directory -Path $dossierChemin | Out-Null
    }
    
    # Nom du fichier avec horodatage
    $date = Get-Date -Format "MM-yyyy-HH-mm"
    $fichierChemin = Join-Path $dossierChemin "$date.html"
    
    # Début du code HTML
    $rapportHTML = @"
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport de Sécurité Système</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f6f7;
            color: #333;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }
        header {
            background: #2980b9;
            color: white;
            text-align: center;
            padding: 20px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        h2 {
            color: #3498db;
            font-size: 1.8em;
            margin-top: 20px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        .section {
            margin: 20px 0;
        }
        .section h3 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .permissions, .admin-users {
            margin-top: 10px;
            background: #ecf0f1;
            padding: 10px;
            border-radius: 5px;
        }
        table {
            width: 100%;
            margin: 10px 0;
            border-collapse: collapse;
        }
        table th, table td {
            padding: 8px;
            border: 1px solid #ccc;
            text-align: left;
        }
        table th {
            background-color: #3498db;
            color: white;
        }
        .error {
            color: #e74c3c;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <header>
        Rapport de Sécurité Système
    </header>
    <div class="container">
        <h2>1. UTILISATEUR COURANT</h2>
        <div class="section">
            <p><strong>Nom:</strong> $env:USERNAME</p>
            <p><strong>Droits administrateur:</strong> $(([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole("Administrator"))</p>
        </div>

        <h2>2. UTILISATEURS AVEC DROITS ADMINISTRATIFS</h2>
        <div class="section admin-users">
"@

    # Ajout des utilisateurs avec droits administratifs
    try {
        $adminUsers = Get-LocalGroupMember -Group "Administrateurs" | Format-Table Name, PrincipalSource -AutoSize | Out-String
        $rapportHTML += "<pre>$adminUsers</pre>"
    }
    catch {
        $rapportHTML += "<p class='error'>Erreur : Impossible de récupérer les utilisateurs administrateurs. Détails : $_</p>"
    }

    $rapportHTML += "<h2>3. PERMISSIONS DES DOSSIERS SYSTEMES</h2>"

    # Ajout des permissions des dossiers critiques
    foreach ($folder in $criticalFolders) {
        $rapportHTML += "<div class='section'><h3>Vérification pour : $folder</h3>"
        
        try {
            # Récupération des permissions
            $acl = Get-Acl $folder -ErrorAction Stop
            $permissions = $acl.Access | Where-Object { 
                $_.IdentityReference -notlike "BUILTIN\*" -and 
                $_.IdentityReference -notlike "NT AUTHORITY\*" 
            } | Format-Table IdentityReference, AccessControlType, FileSystemRights -AutoSize | Out-String
            
            if ($permissions) {
                $rapportHTML += "<pre>$permissions</pre>"
            }
            else {
                $rapportHTML += "<p>Aucune permission personnalisée trouvée.</p>"
            }
        }
        catch {
            $rapportHTML += "<p class='error'>Erreur d'accès au dossier : $_</p>"
        }
        $rapportHTML += "</div>"
    }

    # Fin du rapport HTML
    $rapportHTML += @"
    </div>
</body>
</html>
"@

    # Écriture du rapport HTML dans le fichier avec encodage UTF8
    try {
        $rapportHTML | Out-File -FilePath $fichierChemin -Encoding UTF8 -Force
        Write-Host "Rapport de sécurité créé : $fichierChemin" -ForegroundColor Green
    }
    catch {
        Write-Host "Erreur lors de l'écriture du fichier de rapport : $_" -ForegroundColor Red
    }
}
else {
    Write-Host "Aucun nom de dossier fourni. Script annulé." -ForegroundColor Yellow
}
