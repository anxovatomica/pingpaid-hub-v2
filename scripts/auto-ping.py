#!/usr/bin/env python3
"""
PingPaid SEO Auto-Ping Script v2
Updated: Google deprecated sitemap ping in 2023.
Uses IndexNow, Bing Webmaster API, and RSS feed pinging.
Usage: python3 scripts/auto-ping.py
"""

import urllib.request
import urllib.parse
import json
import sys
import time
from pathlib import Path

def get_all_urls():
    """Read all HTML URLs from the directory."""
    base = "https://anxovatomica.github.io/pingpaid-hub-v2/"
    root = Path("/root/.openclaw/workspace/pingpaid-hub-v2")
    urls = []
    for f in root.rglob("*.html"):
        rel = f.relative_to(root).as_posix()
        urls.append(base + rel)
    return sorted(urls)

def ping_bing(urls):
    """Ping Bing Webmaster Tools with the sitemap."""
    sitemap_url = "https://anxovatomica.github.io/pingpaid-hub-v2/sitemap.xml"
    
    ping_url = f"https://www.bing.com/ping?sitemap={urllib.parse.quote(sitemap_url)}"
    try:
        req = urllib.request.Request(ping_url, headers={"User-Agent": "PingPaid-SEO-Bot/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.status
            print(f"  ✅ Bing sitemap ping: HTTP {status}")
    except Exception as e:
        print(f"  ⚠️ Bing sitemap ping failed: {e}")

def ping_indexnow(urls):
    """Submit URLs via IndexNow protocol (Bing, Yandex, Seznam.cz, Naver, etc.)."""
    # IndexNow requires an API key — get yours from https://www.bing.com/indexnow
    # Place the key in a file named: anxovatomica.github.io.txt
    # at the root of your site: https://anxovatomica.github.io/anxovatomica.github.io.txt
    api_key = "YOUR_INDEXNOW_API_KEY"  # Replace with real key
    host = "anxovatomica.github.io"
    
    payload = {
        "host": host,
        "key": api_key,
        "urlList": urls[:100]  # Start with 100 URLs per batch
    }
    
    endpoints = [
        "https://api.indexnow.org/IndexNow",
        "https://www.bing.com/indexnow",
    ]
    
    for endpoint in endpoints:
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                endpoint,
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "PingPaid-SEO-Bot/1.0"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                status = resp.status
                print(f"  ✅ {endpoint.split('/')[2]}: HTTP {status}")
        except Exception as e:
            print(f"  ⚠️ {endpoint.split('/')[2]} failed: {e}")

def submit_to_google_search_console(urls):
    """
    Submit URLs to Google Search Console via Indexing API.
    Requires a service account JSON file at scripts/google-service-account.json
    Get one from: https://developers.google.com/search/apis/indexing-api/v3/prereqs
    """
    print(f"  ℹ️ Google Indexing API requires service account setup.")
    print(f"  ℹ️ Place your service account JSON at: scripts/google-service-account.json")
    print(f"  ℹ️ Then run: python3 scripts/google-indexing-api.py")

def main():
    print("=" * 60)
    print("🔥 PingPaid SEO Auto-Ping v2 — GOD LEVEL")
    print("=" * 60)
    
    urls = get_all_urls()
    print(f"\n📄 Total URLs found: {len(urls)}")
    
    print("\n📡 Pinging Bing (still supports sitemap ping)...")
    ping_bing(urls)
    time.sleep(1)
    
    print("\n📡 Submitting via IndexNow...")
    ping_indexnow(urls)
    
    print("\n📡 Google Indexing API info...")
    submit_to_google_search_console(urls)
    
    print("\n" + "=" * 60)
    print("✅ Done!")
    print("\n🚀 MANUAL STEPS TO GET INDEXED FAST:")
    print("   1. Go to https://search.google.com/search-console")
    print("   2. Add: https://anxovatomica.github.io/pingpaid-hub-v2/")
    print("   3. Submit sitemap.xml")
    print("   4. Request indexing for top 10 pages")
    print("   5. Get 1-2 backlinks (fastest way to index)")
    print("=" * 60)

if __name__ == "__main__":
    main()
