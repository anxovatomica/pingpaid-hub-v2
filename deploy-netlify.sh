#!/bin/bash
set -e

echo "🚀 PingPaid Hub - Quick Deploy to Netlify"
echo "==========================================="
echo ""

# Check if netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "📦 Installing Netlify CLI..."
    npm install -g netlify-cli
fi

# Check credentials
if [ -z "$NETLIFY_AUTH_TOKEN" ] || [ -z "$NETLIFY_SITE_ID" ]; then
    echo "❌ Missing Netlify credentials!"
    echo ""
    echo "Get your credentials:"
    echo "1. Go to https://app.netlify.com/user/applications/personal"
    echo "2. Generate a personal access token"
    echo "3. Create a new site at https://app.netlify.com"
    echo "4. Get Site ID from Site Settings > General"
    echo ""
    read -p "Enter Netlify Auth Token: " TOKEN
    read -p "Enter Netlify Site ID: " SITE
    export NETLIFY_AUTH_TOKEN="$TOKEN"
    export NETLIFY_SITE_ID="$SITE"
fi

echo "🎯 Deploying to Netlify..."
netlify deploy --prod --dir=. --site=$NETLIFY_SITE_ID

echo ""
echo "✅ DONE! Your site is live!"
echo ""
echo "Next steps for SEO:"
echo "1. Add custom domain in Netlify Site Settings"
echo "2. Go to https://search.google.com/search-console"
echo "3. Add your property and verify"
echo "4. Submit sitemap"
