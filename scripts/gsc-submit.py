#!/usr/bin/env python3
"""
PingPaid Google Search Console + Indexing API Submission
Uses service account to:
1. Submit sitemap to Google Search Console
2. Request indexing for top 10 pages
"""

import json
import sys
from pathlib import Path
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import urllib.request
import urllib.error

# Config
SCOPES = [
    'https://www.googleapis.com/auth/webmasters',
    'https://www.googleapis.com/auth/indexing',
]
SERVICE_ACCOUNT_FILE = '/root/.openclaw/workspace/pingpaid-hub-v2/scripts/google-service-account.json'
SITE_URL = 'https://anxovatomica.github.io/pingpaid-hub-v2/'
SITEMAP_URL = 'https://anxovatomica.github.io/pingpaid-hub-v2/sitemap.xml'

TOP_PAGES = [
    'https://anxovatomica.github.io/pingpaid-hub-v2/',
    'https://anxovatomica.github.io/pingpaid-hub-v2/blog/client-wont-pay.html',
    'https://anxovatomica.github.io/pingpaid-hub-v2/pages/best-invoicing-software-2026.html',
    'https://anxovatomica.github.io/pingpaid-hub-v2/calculator/late-fee-calculator.html',
    'https://anxovatomica.github.io/pingpaid-hub-v2/pages/pingpaid-vs-competitors.html',
    'https://anxovatomica.github.io/pingpaid-hub-v2/blog/invoice-payment-terms.html',
    'https://anxovatomica.github.io/pingpaid-hub-v2/calculator/roi-calculator.html',
    'https://anxovatomica.github.io/pingpaid-hub-v2/pages/designers-invoice.html',
    'https://anxovatomica.github.io/pingpaid-hub-v2/blog/how-to-write-invoice.html',
    'https://anxovatomica.github.io/pingpaid-hub-v2/pages/best-freelance-tools-2026.html',
]

def get_credentials():
    """Load service account credentials."""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    credentials.refresh(Request())
    return credentials

def submit_sitemap(credentials):
    """Submit sitemap to Google Search Console."""
    print("📡 Submitting sitemap to Google Search Console...")
    
    url = f'https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(SITE_URL, safe="")}/sitemaps/{urllib.parse.quote(SITEMAP_URL, safe="")}'
    
    req = urllib.request.Request(
        url,
        method='PUT',
        headers={
            'Authorization': f'Bearer {credentials.token}',
            'Content-Type': 'application/json',
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"  ✅ Sitemap submitted: HTTP {resp.status}")
            return True
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f"  ⚠️ HTTP 403 — Service account not authorized in GSC yet.")
            print(f"  ⚠️ Add {credentials.service_account_email} as owner in GSC.")
        else:
            print(f"  ⚠️ HTTP {e.code}: {e.read().decode()[:200]}")
        return False
    except Exception as e:
        print(f"  ⚠️ Error: {e}")
        return False

def request_indexing(credentials, url):
    """Request indexing for a single URL via Google Indexing API."""
    api_url = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
    
    payload = json.dumps({
        'url': url,
        'type': 'URL_UPDATED'
    }).encode('utf-8')
    
    req = urllib.request.Request(
        api_url,
        data=payload,
        method='POST',
        headers={
            'Authorization': f'Bearer {credentials.token}',
            'Content-Type': 'application/json',
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            print(f"  ✅ {url[:60]}... — HTTP {resp.status}")
            return True
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f"  ⚠️ HTTP 403 — Indexing API not authorized.")
            print(f"  ⚠️ Ensure service account is added to GSC with Owner permission.")
        elif e.code == 429:
            print(f"  ⚠️ HTTP 429 — Rate limited. Wait and retry.")
        else:
            print(f"  ⚠️ HTTP {e.code}: {e.read().decode()[:200]}")
        return False
    except Exception as e:
        print(f"  ⚠️ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("🔥 PingPaid Google Search Console + Indexing API")
    print("=" * 60)
    
    # Load credentials
    print("\n🔐 Loading service account credentials...")
    try:
        credentials = get_credentials()
        print(f"  ✅ Authenticated as: {credentials.service_account_email}")
    except Exception as e:
        print(f"  ❌ Failed to authenticate: {e}")
        sys.exit(1)
    
    # Submit sitemap
    sitemap_ok = submit_sitemap(credentials)
    
    # Request indexing for top pages
    print(f"\n📡 Requesting indexing for {len(TOP_PAGES)} top pages...")
    indexed = 0
    for i, url in enumerate(TOP_PAGES, 1):
        print(f"\n  [{i}/{len(TOP_PAGES)}] {url}")
        if request_indexing(credentials, url):
            indexed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUBMISSION REPORT")
    print("=" * 60)
    print(f"   Sitemap: {'✅ Submitted' if sitemap_ok else '⚠️ Needs GSC authorization'}")
    print(f"   Pages indexed: {indexed}/{len(TOP_PAGES)}")
    
    if not sitemap_ok or indexed == 0:
        print("\n⚠️ ACTION NEEDED:")
        print("   1. Go to https://search.google.com/search-console")
        print("   2. Select your property: " + SITE_URL)
        print("   3. Go to Settings → Users and permissions")
        print("   4. Click 'Add user'")
        print(f"   5. Email: {credentials.service_account_email}")
        print("   6. Permission: Owner")
        print("   7. Click 'Add'")
        print("   8. Re-run this script")
    else:
        print("\n✅ ALL DONE! Google will index these pages within 24-72 hours.")
    
    print("=" * 60)

if __name__ == '__main__':
    main()
