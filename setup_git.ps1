# 1. Initialize Git if not already present
if (-not (Test-Path .git)) {
    git init
    Write-Host "Initialized local Git repository." -ForegroundColor Cyan
} else {
    Write-Host "Git repository already initialized." -ForegroundColor Yellow
}

# 2. Add all files
git add .

# 3. Create initial commit (if changes exist)
$status = git status --porcelain
if ($status) {
    git commit -m "Research update: Audited Persona Simulation (100k Agents)"
} else {
    Write-Host "No changes to commit." -ForegroundColor Cyan
}

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
