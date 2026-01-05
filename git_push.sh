#!/data/data/com.termux/files/usr/bin/bash

# ==============================
# LunaLibrary Git Auto-Push Script
# ==============================

# Start the ssh-agent
eval "$(ssh-agent -s)"

# Add your SSH key (enter passphrase once)
ssh-add ~/.ssh/id_ed25519

# Navigate to LunaLibrary repo
cd ~/LunaLibrary || { echo "LunaLibrary folder not found"; exit 1; }

# Pull latest changes from GitHub
echo "Pulling latest changes..."
git pull origin main

# Add all new or changed files
echo "Adding changes..."
git add .

# Commit changes with timestamp message
commit_msg="Auto-commit: $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$commit_msg"

# Push to GitHub
echo "Pushing to GitHub..."
git push origin main

echo "✅ LunaLibrary synced successfully!"
