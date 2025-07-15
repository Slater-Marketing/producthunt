# ProductHunt Scraper PowerShell Script
# Run this script to execute the ProductHunt scraper

param(
    [switch]$RunOnce,
    [switch]$Schedule
)

# Set execution policy for current session
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Function to run the scraper
function Run-Scraper {
    Write-Host "Starting ProductHunt Scraper at $(Get-Date)" -ForegroundColor Green
    
    try {
        # Check if Python is available
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "Python is not installed or not in PATH"
        }
        Write-Host "Python version: $pythonVersion" -ForegroundColor Yellow
        
        # Check if required packages are installed
        Write-Host "Checking dependencies..." -ForegroundColor Yellow
        python -c "import selenium, schedule, pytz, webdriver_manager" 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Installing required packages..." -ForegroundColor Yellow
            pip install -r requirements.txt
        }
        
        # Run the scraper
        if ($RunOnce) {
            Write-Host "Running scraper once..." -ForegroundColor Yellow
            python producthunt_scraper.py
        } elseif ($Schedule) {
            Write-Host "Starting scheduled scraper..." -ForegroundColor Yellow
            python scheduler.py
        } else {
            Write-Host "Running scraper once..." -ForegroundColor Yellow
            python producthunt_scraper.py
        }
        
        Write-Host "Scraper completed successfully at $(Get-Date)" -ForegroundColor Green
    }
    catch {
        Write-Host "Error running scraper: $_" -ForegroundColor Red
        exit 1
    }
}

# Run the scraper
Run-Scraper 