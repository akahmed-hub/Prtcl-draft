# Initialize git repository
Write-Host "Initializing git repository..." -ForegroundColor Green
git init

# Add all files
Write-Host "Adding files to git..." -ForegroundColor Green
git add .

# Make initial commit
Write-Host "Making initial commit..." -ForegroundColor Green
git commit -m "Initial commit: Full-stack Django + React application with Docker setup

- Django backend with REST API
- React frontend with Material-UI
- PostgreSQL database
- Redis for Celery tasks
- Docker containerization
- Protocol builder, data analysis, and visualization features"

Write-Host ""
Write-Host "✅ Git repository initialized successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Create a new repository on GitHub" -ForegroundColor White
Write-Host "2. Run these commands:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "Replace YOUR_USERNAME and YOUR_REPO_NAME with your actual GitHub details." -ForegroundColor White 