Write-Host "Version actuelle de Python : $(python --version)"
Write-Host "Version actuelle de pip : $(pip --version)"

Function Uninstall-Pip {
    Write-Host "Désinstallation de pip..."
    python -m pip uninstall pip -y
}

Function Install-Pip {
    Write-Host "Réinstallation de pip..."
    python -m ensurepip --upgrade
}

Function Update-Pip {
    Write-Host "Mise à jour de pip..."
    python -m pip install --upgrade --user pip
}

Uninstall-Pip

Install-Pip

Update-Pip

Write-Host "Nouvelle version de Python : $(python --version)"
Write-Host "Nouvelle version de pip : $(pip --version)"

Write-Host "Installation des modules Python : pycvesearch, python-nmap, pyfiglet, paramiko, psutil"

python -m pip install --user tabulate
python -m pip install --user pycvesearch
python -m pip install --user python-nmap
python -m pip install --user pyfiglet
python -m pip install --user paramiko
python -m pip install --user psutil

Write-Host "Modules Python installés avec succès !"
Write-Host "Mise à jour de Python, pip et installation des modules terminée !"
