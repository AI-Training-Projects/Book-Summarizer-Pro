# Git Setup Commands for Book Summarizer Pro

## Local Repository Setup
```bash
# Initialize a new git repository in the current directory
git init

# Rename the default branch from 'master' to 'main'
git branch -m master main

## Set the default branch for new repositories
# git config --global init.defaultBranch main

# Add all files to staging (except those in .gitignore)
git add .

# Create the initial commit with all your files
git commit -m "Initial commit: Book Summarizer Pro application"
```

## GitHub Repository Setup
1. Go to: https://github.com/orgs/AI-Training-Projects/new
2. Fill in:
   - Repository name: book-summarizer-pro
   - Description: Flask-based application for summarizing books and documents using NLP
   - Visibility: Private (recommended for development)
   - Don't initialize with README (we already have one)

## Link Local to GitHub Repository
```bash
# Add the GitHub repository as remote
git remote add origin https://github.com/AI-Training-Projects/book-summarizer-pro.git

# Verify the remote was added correctly
git remote -v

# Push your code to GitHub (main branch)
git push -u origin main
```

## Common Daily Commands
```bash
# Check repository status
git status

# Pull latest changes from GitHub
git pull origin main

# Create a new branch for a feature
git checkout -b feature/new-feature-name

# Switch between branches
git checkout main

# Stage changes for commit
git add <filename>    # Stage specific file
git add .            # Stage all changes

# Commit changes
git commit -m "Description of changes"

# Push changes to GitHub
git push origin <branch-name>
```

## Collaboration Commands
```bash
# Update your local repository with remote changes
git fetch origin

# Merge changes from main into your feature branch
git checkout feature/your-branch
git merge origin/main

# Create a pull request
# This is done through the GitHub web interface:
# 1. Go to https://github.com/AI-Training-Projects/book-summarizer-pro
# 2. Click "Pull requests"
# 3. Click "New pull request"
# 4. Select your branch and create the PR
```

## Useful Git Configurations
```bash
# Set your identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch name to main
git config --global init.defaultBranch main

# Configure line ending handling (important for Windows)
git config --global core.autocrlf true
```

## Important Notes
1. Always pull before starting new work
2. Create feature branches for new work
3. Write clear commit messages
4. Review changes before committing
5. Keep commits focused and atomic
6. Use .gitignore to exclude sensitive files

## Security Reminders
- Never commit sensitive data (.env files, API keys, passwords)
- Review code before pushing to ensure no secrets are exposed
- Use environment variables for sensitive information
- Keep the .gitignore file up to date
