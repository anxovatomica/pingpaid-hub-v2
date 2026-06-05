#!/bin/bash
set -e

echo "🚀 PingPaid Hub - Quick Deploy to Cloudflare Pages"
echo "===================================================="
echo ""
echo "Cloudflare Pages = BEST for SEO (fastest CDN, unlimited bandwidth, free SSL)"
echo ""

# Check if wrangler is installed
if ! command -v wrangler &> /dev/null; then
    echo "📦 Installing Cloudflare Wrangler..."
    npm install -g wrangler
fi

# Check credentials
if [ -z "$CLOUDFLARE_API_TOKEN" ] || [ -z "$CLOUDFLARE_ACCOUNT_ID" ]; then
    echo "❌ Missing Cloudflare credentials!"
    echo ""
    echo "Get your credentials:"
    echo "1. Go to https://dash.cloudflare.com/profile/api-tokens"
    echo "2. Create token with 'Cloudflare Pages:Edit' permission"
    echo "3. Find Account ID at https://dash.cloudflare.com (right sidebar)"
    echo ""
    read -p "Enter Cloudflare API Token: " TOKEN
    read -p "Enter Cloudflare Account ID: " ACCOUNT
    export CLOUDFLARE_API_TOKEN="$TOKEN"
    export CLOUDFLARE_ACCOUNT_ID="$ACCOUNT"
fi

echo "🎯 Deploying to Cloudflare Pages..."
npx wrangler pages deploy . --project-name=pingpaid-hub

echo ""
echo "✅ DONE! Your site is live at:"
echo "🌐 https://pingpaid-hub.pages.dev"
echo ""
echo "Next steps for SEO:"
echo "1. Add custom domain in Cloudflare Pages dashboard"
echo "2. Go to https://search.google.com/search-console"
echo "3. Add your property and verify"
echo "4. Submit sitemap: https://pingpaid-hub.pages.dev/sitemap.xml"
echo ""
