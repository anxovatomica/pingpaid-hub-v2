#!/bin/bash
set -e

echo "🚀 PingPaid Hub Deployment Script"
echo "================================="
echo ""

# Check for available credentials
HAS_CLOUDFLARE=false
HAS_NETLIFY=false
HAS_SURGE=false

if [ -n "$CLOUDFLARE_API_TOKEN" ] && [ -n "$CLOUDFLARE_ACCOUNT_ID" ]; then
    HAS_CLOUDFLARE=true
fi

if [ -n "$NETLIFY_AUTH_TOKEN" ] && [ -n "$NETLIFY_SITE_ID" ]; then
    HAS_NETLIFY=true
fi

if [ -f "$HOME/.surge" ] || [ -n "$SURGE_TOKEN" ]; then
    HAS_SURGE=true
fi

# Show available options
echo "Available platforms:"
if [ "$HAS_CLOUDFLARE" = true ]; then
    echo "  ✅ Cloudflare Pages (Recommended - Best SEO)"
else
    echo "  ⚠️  Cloudflare Pages (needs CLOUDFLARE_API_TOKEN + CLOUDFLARE_ACCOUNT_ID)"
fi

if [ "$HAS_NETLIFY" = true ]; then
    echo "  ✅ Netlify"
else
    echo "  ⚠️  Netlify (needs NETLIFY_AUTH_TOKEN + NETLIFY_SITE_ID)"
fi

if [ "$HAS_SURGE" = true ]; then
    echo "  ✅ Surge.sh"
else
    echo "  ⚠️  Surge.sh (needs login: surge login)"
fi

echo ""

# If no credentials, show setup instructions
if [ "$HAS_CLOUDFLARE" = false ] && [ "$HAS_NETLIFY" = false ] && [ "$HAS_SURGE" = false ]; then
    echo "❌ No deployment credentials found!"
    echo ""
    echo "To deploy, you need to set up one of these platforms:"
    echo ""
    echo "1. Cloudflare Pages (BEST for SEO - Recommended):"
    echo "   - Get API token: https://dash.cloudflare.com/profile/api-tokens"
    echo "   - Create token with 'Cloudflare Pages:Edit' permission"
    echo "   - Get Account ID from dashboard right sidebar"
    echo "   - Run: export CLOUDFLARE_API_TOKEN=your_token"
    echo "   - Run: export CLOUDFLARE_ACCOUNT_ID=your_account_id"
    echo ""
    echo "2. Netlify:"
    echo "   - Get token: https://app.netlify.com/user/applications/personal"
    echo "   - Create site at https://app.netlify.com"
    echo "   - Run: export NETLIFY_AUTH_TOKEN=your_token"
    echo "   - Run: export NETLIFY_SITE_ID=your_site_id"
    echo ""
    echo "3. Surge.sh:"
    echo "   - Run: npx surge login"
    echo "   - Enter email and password"
    echo ""
    echo "After setting credentials, run this script again."
    exit 1
fi

# Deploy to preferred platform (Cloudflare first)
if [ "$HAS_CLOUDFLARE" = true ]; then
    echo "🎯 Deploying to Cloudflare Pages (Best for SEO)..."
    npx wrangler pages deploy . --project-name=pingpaid-hub
    echo "✅ Deployed to Cloudflare Pages!"
    echo "🌐 Your site will be at: https://pingpaid-hub.pages.dev"
    exit 0
fi

if [ "$HAS_NETLIFY" = true ]; then
    echo "🎯 Deploying to Netlify..."
    npx netlify deploy --prod --dir=. --site=$NETLIFY_SITE_ID
    echo "✅ Deployed to Netlify!"
    exit 0
fi

if [ "$HAS_SURGE" = true ]; then
    echo "🎯 Deploying to Surge.sh..."
    npx surge . pingpaid-hub.surge.sh
    echo "✅ Deployed to Surge.sh!"
    echo "🌐 Your site is at: https://pingpaid-hub.surge.sh"
    exit 0
fi
