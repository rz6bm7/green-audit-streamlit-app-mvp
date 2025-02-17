# fix_tokenizers.ps1
# This script automates the installation and update of dependencies needed for tokenizers

# Log File Path
$LogFile = ".\fix_tokenizers.log"

# Logging Function
function Write-Log {
    param ([string]$Message)
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $LogFile -Value "$Timestamp - $Message"
    Write-Host "$Timestamp - $Message"
}

Write-Log "Starting Fix Tokenizers Script..."

# Ensure Execution Policy is set correctly for this session
$executionPolicy = Get-ExecutionPolicy -Scope Process
if ($executionPolicy -ne "Bypass") {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    Write-Log "Execution Policy set to Bypass for this session."
}

# Define possible Python installation paths
$PythonPaths = @(
    "C:\Users\rz6bm\AppData\Local\Programs\Python\Python312\python.exe",
    "C:\Python312\python.exe",
    "C:\Python\python.exe"
)

$PythonPath = $null
foreach ($Path in $PythonPaths) {
    if (Test-Path $Path) {
        $PythonPath = $Path
        break
    }
}

if (-not $PythonPath) {
    Write-Log "Python not found at expected paths. Attempting to detect system Python..."
    $PythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
}

if ($PythonPath) {
    Write-Log "Python found at: $PythonPath"
} else {
    Write-Log "ERROR: Python is not installed or cannot be found."
    exit 1
}

# Ensure pip is installed
Write-Log "Checking for pip..."
$PipCheck = & $PythonPath -m pip --version 2>&1
if ($PipCheck -match "No module named pip") {
    Write-Log "pip not found. Installing pip..."
    & $PythonPath -m ensurepip --default-pip
    & $PythonPath -m pip install --upgrade pip
} else {
    Write-Log "pip is installed."
}

# Check for Rust and Cargo
Write-Log "Checking for Rust and Cargo..."
$CargoPath = (Get-Command cargo -ErrorAction SilentlyContinue).Source
if (-not $CargoPath) {
    Write-Log "ERROR: Rust and Cargo not found. Install Rust manually."
    exit 1
} else {
    Write-Log "Rust and Cargo found."
}

# Check for Visual Studio Build Tools via reg
