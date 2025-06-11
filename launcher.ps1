# Encoding: UTF-8
# Définition des chemins des scripts Python
$scanlocal = "E:\Hawkey\scan_local_logiciel.py"
$scanreseau = "E:\Hawkey\scan_network.py"

# Exécuter le premier script Python et attendre qu'il se termine
Write-Host "[INFO] Execution of $scanlocal..."
python $scanlocal
Write-Host "[INFO] $scanlocal termined."

# Exécuter le second script Python et attendre qu'il se termine
Write-Host "[INFO] Execution of $scanreseau..."
python $scanreseau
Write-Host "[INFO] $scanreseau termined."

Write-Host "[INFO] All scripts were executed successfully."