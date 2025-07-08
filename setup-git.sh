#!/bin/bash

# Initialize git repository
echo "Initializing git repository..."
git init

# Add all files
echo "Adding files to git..."
git add .

# Make initial commit
echo "Making initial commit..."
git commit -m "Initial commit: Full-stack Django + React application with Docker setup

- Django backend with REST API
- React frontend with Material-UI
- PostgreSQL database
- Redis for Celery tasks
- Docker containerization
- Protocol builder, data analysis, and visualization features"

echo ""
echo "✅ Git repository initialized successfully!"
echo ""
echo "Next steps:"
echo "1. Create a new repository on GitHub"
echo "2. Run these commands:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "Replace YOUR_USERNAME and YOUR_REPO_NAME with your actual GitHub details." 