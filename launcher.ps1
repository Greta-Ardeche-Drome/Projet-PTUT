# Définition des chemins des scripts
$scanlocal = "C:\Users\Iutuser\Documents\Projet PTUT Script\postscanlocal.ps1"
$scanreseau = "C:\Users\Iutuser\Documents\Projet PTUT Script\scan_network.py"

# Exécuter le premier script PowerShell et attendre qu'il se termine
Write-Host "[INFO] Exécution de $scanlocal..."
& $scanlocal
Write-Host "[INFO] $scanlocal terminé."

# Exécuter le second script Python et attendre qu'il se termine
Write-Host "[INFO] Exécution de $scanreseau..."
python $scanreseau
Write-Host "[INFO] $scanreseau terminé."

Write-Host "[INFO] Tous les scripts ont été exécutés avec succès."
