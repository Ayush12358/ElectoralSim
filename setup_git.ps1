# Electoral Simulation Project - Git Setup Script (Windows PowerShell)

# 1. Initialize Git
git init

# 2. Add all files
git add .

# 3. Create initial commit
git commit -m "Initial research release: Stability-Proportionality Simulation (1:10 Scale)"

# 4. Prompt for Remote URL
Write-Host "Please enter your GitHub repository URL (e.g., https://github.com/ayush-maurya/electoral-simulation-india.git):" -ForegroundColor Green
$remoteUrl = Read-Host

if ($remoteUrl) {
    git remote add origin $remoteUrl
    Write-Host "Attempting to push to main..." -ForegroundColor Cyan
    git branch -M main
    git push -u origin main
} else {
    Write-Host "No URL provided. Git initialized locally." -ForegroundColor Red
}
