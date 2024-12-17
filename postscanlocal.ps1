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
    $fichierChemin = Join-Path $dossierChemin "$date.txt"
    
    # Préparer le rapport complet
    $rapportComplet = @"
FULL SYSTEM SECURITY REPORT
===================================

1. UTILISATEUR COURANT
---------------------
Nom : $env:USERNAME
Droits administrateur : $(([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole("Administrator"))

2. UTILISATEURS AVEC DROITS ADMINISTRATIFS
-----------------------------------------
"@

    # Ajout des utilisateurs avec droits administratifs
    try {
        $adminUsers = Get-LocalGroupMember -Group "Administrateurs" | Format-Table Name, PrincipalSource -AutoSize | Out-String
        $rapportComplet += "`n$adminUsers"
    }
    catch {
        $rapportComplet += "`nErreur : Impossible de récupérer les utilisateurs administrateurs. Détails : $_"
    }

    # Ajout des permissions des dossiers critiques
    $rapportComplet += "`n`nPERMISSIONS DES DOSSIERS SYSTEMES"
    $rapportComplet += "`n================================="

    foreach ($folder in $criticalFolders) {
        $rapportComplet += "`n`nVérification pour : $folder"
        $rapportComplet += "`n---------------------------------"
        
        try {
            # Récupération des permissions
            $acl = Get-Acl $folder -ErrorAction Stop
            $permissions = $acl.Access | Where-Object { 
                $_.IdentityReference -notlike "BUILTIN\*" -and 
                $_.IdentityReference -notlike "NT AUTHORITY\*" 
            } | Format-Table IdentityReference, AccessControlType, FileSystemRights -AutoSize | Out-String
            
            if ($permissions) {
                $rapportComplet += $permissions
            }
            else {
                $rapportComplet += "`nAucune permission personnalisée trouvée."
            }
        }
        catch {
            $rapportComplet += "`nErreur d'accès au dossier : $_"
        }
    }

    # Écriture du rapport dans le fichier avec encodage UTF8
    try {
        $rapportComplet | Out-File -FilePath $fichierChemin -Encoding UTF8 -Force
        Write-Host "Rapport de sécurité créé : $fichierChemin" -ForegroundColor Green
    }
    catch {
        Write-Host "Erreur lors de l'écriture du fichier de rapport : $_" -ForegroundColor Red
    }
}
else {
    Write-Host "Aucun nom de dossier fourni. Script annulé." -ForegroundColor Yellow
}
