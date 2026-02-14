#!/bin/bash

# Railway Deployment Script
# This script helps you deploy to Railway

echo "🚀 Railway Deployment Helper"
echo "============================"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

echo "✅ Railway CLI ready"
echo ""
echo "Next steps:"
echo "1. Run: railway login"
echo "2. Run: railway init"
echo "3. Set environment variables in Railway dashboard"
echo "4. Run: railway up"
echo ""
echo "Or deploy via Railway web dashboard:"
echo "1. Go to https://railway.app"
echo "2. New Project → Deploy from GitHub"
echo "3. Select your repository"
echo "4. Add environment variables"
echo ""

