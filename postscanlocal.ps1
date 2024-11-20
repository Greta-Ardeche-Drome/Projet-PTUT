$criticalFolders = @(
    "C:\Windows",
    "C:\Windows\System32", 
    "C:\Program Files",
    "C:\Program Files (x86)", 
    "C:\Users",
    "C:\Windows\System32\Config", 
    "C:\Windows\Temp"
)

Add-Type -AssemblyName Microsoft.VisualBasic
$dossierNom = [Microsoft.VisualBasic.Interaction]::InputBox("Quel nom voulez-vous donner au dossier de rapport ?", "Scan Permissions", "")

if ($dossierNom) {
    $basePath = "C:\Users\Iutuser\Documents\Projet PTUT Script"
    $dossierChemin = Join-Path $basePath $dossierNom
    
    if (!(Test-Path $dossierChemin)) {
        New-Item -Type Directory $dossierChemin | Out-Null
    }
    
    $date = Get-Date -Format "MM-yyyy-HH-mm"
    $fichierChemin = Join-Path $dossierChemin "$date.txt"
    
    # Préparer le rapport complet
    $rapportComplet = @"
FULL SYSTEM SECURITY REPORT
===================================

1. UTILISATEUR COURANT
---------------------
Nom : $env:USERNAME
Droits administrateur :$(([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole("Administrator"))

2. UTILISATEURS AVEC DROITS ADMINISTRATIFS
-----------------------------------------
"@

    # Ajouter les utilisateurs administrateurs
    $rapportComplet += "`n" + ((Get-LocalGroupMember -Group "Administrateurs" | Format-Table -AutoSize | Out-String))

    $rapportComplet += "`nPERMISSIONS DES DOSSIERS SYSTEMES"
    $rapportComplet += "`n================================="

    foreach ($folder in $criticalFolders) {
        $rapportComplet += "`nVerification for: $folder"
        $rapportComplet += "`n---------------------------------"
        
        try {
            $acl = Get-Acl $folder
            $permissions = $acl.Access | Where-Object { 
                $_.IdentityReference -notlike "BUILTIN\*" -and 
                $_.IdentityReference -notlike "NT AUTHORITY\*" 
            } | Format-Table IdentityReference, AccessControlType, FileSystemRights -AutoSize | Out-String
            
            $rapportComplet += $permissions
        }
        catch {
            $rapportComplet += "`nErreur de lecture : $_"
        }
    }

    # Écrire le rapport dans le fichier
    $rapportComplet | Out-File $fichierChemin
    
    Write-Host "Security report create : $fichierChemin"
} else {
    Write-Host "No name provided. Script cancelled."
}