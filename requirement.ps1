Write-Host "Current version of Python : $(python --version)"
Write-Host "Current version of pip : $(pip --version)"

Function Uninstall-Pip {
    Write-Host "Uninstalling pip..."
    python -m pip uninstall pip -y
}

Function Install-Pip {
    Write-Host "Reinstalling pip..."
    python -m ensurepip --upgrade
}

Function Update-Pip {
    Write-Host "pip update..."
    python -m pip install --upgrade --user pip
}

Function Install-Nmap {
    Write-Host "Checking for Nmap presence..."

    $nmapPath = (Get-Command nmap.exe -ErrorAction SilentlyContinue).Source
    if ($nmapPath) {
        Write-Host "Nmap is already installed : $nmapPath"
    } else {
        Write-Host "Nmap is not installed. Downloading and installing..."
        $nmapInstallerUrl = "https://nmap.org/dist/nmap-7.94-setup.exe"
        $installerPath = "$env:TEMP\nmap-setup.exe"

        Invoke-WebRequest -Uri $nmapInstallerUrl -OutFile $installerPath
        Start-Process -FilePath $installerPath -ArgumentList "/S" -Wait

        if (Get-Command nmap.exe -ErrorAction SilentlyContinue) {
            Write-Host "Nmap was installed successfully."
        } else {
            Write-Warning "Nmap installation failed."
        }
    }
}

Uninstall-Pip
Install-Pip
Update-Pip

Write-Host "New version of Python : $(python --version)"
Write-Host "New version of pip : $(pip --version)"

Write-Host "Installing Python Modules : pycvesearch, python-nmap, pyfiglet, paramiko, psutil"

python -m pip install --user tabulate
python -m pip install --user pycvesearch
python -m pip install --user python-nmap
python -m pip install --user pyfiglet
python -m pip install --user paramiko
python -m pip install --user psutil

Install-Nmap

Write-Host "Python modules successfully installed !"
Write-Host "Python, pip, and module installation + Nmap complete!"