
@echo off
echo ==========================================
echo       Setting up GitHub Repository
echo ==========================================

REM 1. Initialize Git (already done, but safe to re-run)
git init

REM 2. Check if logged in to GH
echo Checking GitHub authentication...
gh auth status >nul 2>&1
if %errorlevel% neq 0 (
    echo You are not logged in to GitHub CLI.
    echo Please follow the prompts to login...
    gh auth login
)

REM 3. Create Request
echo Creating repository 'AI-PHONEBOOK' on GitHub...
gh repo create "AI-PHONEBOOK" --private --source=. --remote=origin

REM 4. Add files and Commit (Safe check)
git add .
git commit -m "Initial commit for AI Phonebook" 2>nul

REM 5. Push
echo Pushing code to main branch...
git push -u origin master
git push -u origin main

echo ==========================================
echo          Deployment Complete!
echo ==========================================
pause
