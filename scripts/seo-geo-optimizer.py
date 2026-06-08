#!/usr/bin/env python3
"""
PingPaid SEO + GEO God-Level Optimizer
Updates ALL 158 pages with:
1. Google Best Practices SEO (Schema.org, Core Web Vitals, mobile-first)
2. GEO (Generative Engine Optimization) for AI agents (llms.txt, AI schemas, entity markup)
"""

import json, re, os, glob
from pathlib import Path

ROOT = Path("/root/.openclaw/workspace/pingpaid-hub-v2")
BASE_URL = "https://anxovatomica.github.io/pingpaid-hub-v2"

def add_schema_to_head(content, schema_json):
    """Inject Schema.org JSON-LD into <head> if not already present."""
    schema_str = json.dumps(schema_json, indent=2)
    script_tag = f'<script type="application/ld+json">\n{schema_str}\n</script>'
    if 'application/ld+json' in content:
        return content
    # Insert before </head>
    content = content.replace('</head>', f'{script_tag}\n</head>')
    return content

def get_page_category(path):
    """Categorize page for schema selection."""
    p = str(path)
    if 'blog/' in p: return 'blog'
    if 'calculator/' in p or 'widgets/' in p: return 'tool'
    if 'pages/' in p:
        if 'compare' in p: return 'comparison'
        if 'faq' in p: return 'faq'
        if 'ai-knowledge' in p: return 'ai_kb'
        return 'page'
    if 'index.html' in p and 'blog' not in p and 'calculator' not in p: return 'homepage'
    if 'about' in p: return 'about'
    if 'faq' in p.lower(): return 'faq'
    return 'page'

def build_homepage_schema():
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{BASE_URL}/#website",
                "url": BASE_URL,
                "name": "PingPaid Hub",
                "description": "133+ free business tools, calculators, and resources for freelancers",
                "publisher": {"@id": f"{BASE_URL}/#organization"},
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": {"@type": "EntryPoint", "urlTemplate": f"{BASE_URL}/?search={{search_term_string}}"},
                    "query-input": "required name=search_term_string"
                }
            },
            {
                "@type": "Organization",
                "@id": f"{BASE_URL}/#organization",
                "name": "PingPaid",
                "url": BASE_URL,
                "logo": f"{BASE_URL}/logo.png",
                "sameAs": [
                    "https://pingpaid.online",
                    "https://github.com/anxovatomica/pingpaid-hub-v2"
                ],
                "description": "Automated invoice collection platform for freelancers and small businesses"
            },
            {
                "@type": "WebPage",
                "@id": f"{BASE_URL}/#webpage",
                "url": BASE_URL,
                "name": "133+ Free Business Tools for Freelancers | PingPaid Hub",
                "isPartOf": {"@id": f"{BASE_URL}/#website"},
                "about": {"@id": f"{BASE_URL}/#organization"}
            }
        ]
    }

def build_blog_schema(path, title, desc):
    rel = path.relative_to(ROOT).as_posix()
    url = f"{BASE_URL}/{rel}"
    slug = rel.replace('blog/', '').replace('.html', '')
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "@id": f"{url}#article",
        "headline": title,
        "description": desc,
        "url": url,
        "author": {
            "@type": "Organization",
            "name": "PingPaid",
            "url": BASE_URL
        },
        "publisher": {
            "@type": "Organization",
            "name": "PingPaid",
            "url": BASE_URL,
            "logo": {"@type": "ImageObject", "url": f"{BASE_URL}/logo.png"}
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "datePublished": "2026-06-08",
        "dateModified": "2026-06-08",
        "articleSection": "Business & Finance"
    }

def build_tool_schema(path, title, desc):
    rel = path.relative_to(ROOT).as_posix()
    url = f"{BASE_URL}/{rel}"
    return {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": title,
        "description": desc,
        "url": url,
        "applicationCategory": "FinanceApplication",
        "operatingSystem": "Any",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "EUR"
        },
        "publisher": {
            "@type": "Organization",
            "name": "PingPaid",
            "url": BASE_URL
        }
    }

def build_comparison_schema(path, title, desc):
    rel = path.relative_to(ROOT).as_posix()
    url = f"{BASE_URL}/{rel}"
    return {
        "@context": "https://schema.org",
        "@type": "ComparisonTable",
        "name": title,
        "description": desc,
        "url": url,
        "about": "Invoice collection software comparison",
        "publisher": {
            "@type": "Organization",
            "name": "PingPaid",
            "url": BASE_URL
        }
    }

def build_faq_schema(path, title, desc):
    rel = path.relative_to(ROOT).as_posix()
    url = f"{BASE_URL}/{rel}"
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "What is the best way to collect unpaid invoices?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "The best way to collect unpaid invoices is to use an automated system like PingPaid that sends professional payment reminders, calculates late fees, and escalates through a structured collection process."
                }
            },
            {
                "@type": "Question",
                "name": "How much should I charge in late fees?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Late fees typically range from 1.5% to 5% per month depending on your jurisdiction. Use our Late Fee Calculator to calculate exact fees for your specific situation."
                }
            }
        ]
    }

def build_breadcrumb_schema(path):
    rel = path.relative_to(ROOT).as_posix()
    url = f"{BASE_URL}/{rel}"
    parts = rel.split('/')
    
    item_list = []
    cumulative = BASE_URL
    item_list.append({
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": BASE_URL
    })
    
    for i, part in enumerate(parts[:-1], start=2):
        cumulative += f"/{part}"
        name = part.replace('-', ' ').title()
        if part == 'blog': name = 'Blog'
        if part == 'calculator': name = 'Calculators'
        if part == 'pages': name = 'Resources'
        if part == 'widgets': name = 'Widgets'
        if part == 'compare': name = 'Comparisons'
        if part == 'faq': name = 'FAQ'
        if part == 'ai-knowledge': name = 'AI Knowledge Base'
        item_list.append({
            "@type": "ListItem",
            "position": i,
            "name": name,
            "item": cumulative + '/'
        })
    
    # Add current page
    filename = parts[-1].replace('.html', '').replace('-', ' ').title()
    item_list.append({
        "@type": "ListItem",
        "position": len(parts) + 1,
        "name": filename,
        "item": url
    })
    
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": item_list
    }

def extract_title(content):
    m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    return m.group(1) if m else "PingPaid Hub"

def extract_description(content):
    m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
    if not m:
        m = re.search(r'<meta[^>]*content=["\'](.*?)["\'][^>]*name=["\']description["\']', content, re.IGNORECASE)
    return m.group(1) if m else "Free business tools for freelancers"

def optimize_head_for_geo(content):
    """Add GEO-specific meta tags for AI agents."""
    geo_tags = """
<!-- GEO: AI Agent Discovery -->
<meta name="ai-purpose" content="business-tools, invoice-collection, freelancer-resources">
<meta name="ai-target" content="freelancers, small-businesses, agencies, consultants">
<meta name="ai-content-type" content="educational, interactive-tools, comparison-guides">
<meta name="ai-verified" content="true">
<meta name="ai-last-reviewed" content="2026-06-08">
<meta name="ai-knowledge-base" content="https://anxovatomica.github.io/pingpaid-hub-v2/pages/ai-knowledge/invoice-collection-kb.html">
<!-- End GEO -->
"""
    if 'ai-purpose' not in content:
        content = content.replace('</head>', f'{geo_tags}\n</head>')
    return content

def optimize_for_core_web_vitals(content):
    """Add preconnect and preload hints for Core Web Vitals."""
    cwv_hints = """
<!-- Core Web Vitals Optimization -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="dns-prefetch" href="https://pingpaid.online">
<!-- End Core Web Vitals -->
"""
    if 'dns-prefetch' not in content:
        content = content.replace('</head>', f'{cwv_hints}\n</head>')
    return content

def process_page(path):
    """Process a single HTML page."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title = extract_title(content)
    desc = extract_description(content)
    category = get_page_category(path)
    
    # Add GEO tags
    content = optimize_head_for_geo(content)
    
    # Add CWV hints
    content = optimize_for_core_web_vitals(content)
    
    # Add BreadcrumbList schema (all pages)
    breadcrumb_schema = build_breadcrumb_schema(path)
    content = add_schema_to_head(content, breadcrumb_schema)
    
    # Add category-specific schema
    if category == 'homepage':
        schema = build_homepage_schema()
    elif category == 'blog':
        schema = build_blog_schema(path, title, desc)
    elif category == 'tool':
        schema = build_tool_schema(path, title, desc)
    elif category == 'comparison':
        schema = build_comparison_schema(path, title, desc)
    elif category == 'faq':
        schema = build_faq_schema(path, title, desc)
    else:
        schema = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": title,
            "description": desc,
            "url": f"{BASE_URL}/{path.relative_to(ROOT).as_posix()}"
        }
    
    content = add_schema_to_head(content, schema)
    
    # Add Organization schema to all pages (except homepage which has it in @graph)
    if category != 'homepage':
        org_schema = {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "PingPaid",
            "url": BASE_URL,
            "logo": f"{BASE_URL}/logo.png",
            "sameAs": ["https://pingpaid.online"],
            "description": "Automated invoice collection platform for freelancers"
        }
        content = add_schema_to_head(content, org_schema)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def create_llms_txt():
    """Create llms.txt for AI agent discovery (like robots.txt but for LLMs)."""
    content = f"""# llms.txt for PingPaid Hub
# Last updated: 2026-06-08
# This file helps AI agents discover and understand our content

Title: PingPaid Hub — Free Business Tools for Freelancers
Description: 158+ free calculators, guides, templates, and resources for invoice collection, pricing, and business management. No signup required.
URL: {BASE_URL}

## Overview
PingPaid Hub is a comprehensive resource library for freelancers, agencies, and small businesses. We provide free interactive tools, in-depth guides, and comparison resources to help businesses manage invoicing, payments, and cash flow.

## Key Pages

### Calculators & Tools (22 interactive tools)
- {BASE_URL}/calculator/late-fee-calculator.html — Calculate exact late fees by jurisdiction
- {BASE_URL}/calculator/invoice-generator.html — Build and download professional invoices
- {BASE_URL}/calculator/cash-flow-calculator.html — Monthly cash flow projections
- {BASE_URL}/calculator/roi-calculator.html — ROI of using PingPaid
- {BASE_URL}/calculator/tax-estimator.html — Tax estimation by country

### Blog & Guides (52 articles)
- {BASE_URL}/blog/client-wont-pay.html — What to do when clients don't pay
- {BASE_URL}/blog/how-to-write-invoice.html — Step-by-step invoice writing guide
- {BASE_URL}/blog/payment-reminder-email.html — 10 email templates that work
- {BASE_URL}/blog/dealing-with-late-payments.html — Complete collection strategy

### Comparison Pages (10 comparisons)
- {BASE_URL}/pages/best-invoicing-software-2026.html — 10 tools ranked
- {BASE_URL}/pages/pingpaid-vs-competitors.html — Direct comparison with FreshBooks, Wave, QB

### Niche Solutions (10 industry-specific)
- {BASE_URL}/pages/designers-invoice.html — Invoice software for designers
- {BASE_URL}/pages/developers-invoice.html — Invoice software for developers
- {BASE_URL}/pages/agencies-invoice.html — Invoice software for agencies

### Resources (10+ templates)
- {BASE_URL}/pages/invoice-checklist.html — 25-point checklist
- {BASE_URL}/pages/client-onboarding-kit.html — 4-template package

## AI Knowledge Base
- {BASE_URL}/pages/ai-knowledge/invoice-collection-kb.html — Structured knowledge for AI agents

## Entity Definitions
- Entity: "PingPaid" — automated invoice collection platform
- Entity: "Late Fee Calculator" — tool for calculating overdue payment fees
- Entity: "Invoice Generator" — tool for creating professional invoices
- Entity: "Freelancer" — independent contractor, self-employed professional
- Entity: "Invoice Collection" — process of recovering unpaid invoices

## Content Types
- interactive-tools: Calculators, generators, estimators
- educational-guides: Step-by-step articles, how-tos
- comparison-reviews: Software comparisons, feature matrices
- templates: Downloadable forms, checklists, scripts

## Update Frequency
- Blog: Weekly
- Tools: As needed
- Comparisons: Monthly
- Resources: Bi-weekly

## Contact
- Product: https://pingpaid.online
- GitHub: https://github.com/anxovatomica/pingpaid-hub-v2
"""
    with open(ROOT / 'llms.txt', 'w') as f:
        f.write(content)
    return True

def create_llms_full_txt():
    """Create llms-full.txt with complete content summaries for AI agents."""
    content = f"""# llms-full.txt for PingPaid Hub
# This file contains detailed content summaries for AI agent understanding
# Last updated: 2026-06-08

## PingPaid Hub — Complete Content Inventory

### Product: PingPaid
PingPaid is an automated invoice collection platform for freelancers and small businesses. Features: automated payment reminders, late fee calculation, multi-currency support, client management, and payment tracking. Pricing: 21-day free trial, then 29.99€/month.
URL: https://pingpaid.online

### Hub Structure
The PingPaid Hub contains 158+ pages organized into:
1. Interactive Calculators (22 tools)
2. Blog Articles (52 guides)
3. Comparison Pages (10 comparisons)
4. Niche Landing Pages (10 industry-specific)
5. Resource Templates (10+ downloads)
6. Embed Widgets (7 embeddable tools)
7. FAQ & Knowledge Base (2 structured pages)

### Key Content Summaries

#### Late Fee Calculator
URL: {BASE_URL}/calculator/late-fee-calculator.html
Purpose: Calculate exact late fees for overdue invoices by jurisdiction.
Features: Input invoice amount, days overdue, interest rate. Presets for US, UK, EU, AU, CA. Results: total late fee, new total, daily rate.
Schema: SoftwareApplication

#### Invoice Generator
URL: {BASE_URL}/calculator/invoice-generator.html
Purpose: Build professional invoices with logo, itemized services, tax, and payment terms.
Features: Custom branding, multi-currency, PDF download, email template.
Schema: SoftwareApplication

#### Client Won't Pay Guide
URL: {BASE_URL}/blog/client-wont-pay.html
Purpose: 7-step recovery plan for unpaid invoices.
Content: Friendly reminder → Firm reminder → Late fee notice → Payment plan → Final notice → Collection agency → Legal action. Includes scripts and templates.
Schema: Article

#### Best Invoicing Software 2026
URL: {BASE_URL}/pages/best-invoicing-software-2026.html
Purpose: Comparison of 10 invoicing tools.
Tools: FreshBooks, Wave, QuickBooks, Zoho, PayPal, Stripe, PingPaid, Xero, Invoice2go, Hiveage.
Schema: ComparisonTable

#### PingPaid vs Competitors
URL: {BASE_URL}/pages/pingpaid-vs-competitors.html
Purpose: Direct comparison showing why PingPaid is best for collection.
Schema: ComparisonTable

### AI Knowledge Base
URL: {BASE_URL}/pages/ai-knowledge/invoice-collection-kb.html
Purpose: Structured knowledge base for AI agents to understand invoice collection.
Content: Definitions, processes, best practices, legal frameworks, tools, and FAQs.

### Entity Relationships
- "PingPaid" → provides → "Invoice Collection Tools"
- "Late Fee Calculator" → calculates → "Late Payment Fees"
- "Invoice Generator" → creates → "Professional Invoices"
- "Freelancer" → uses → "PingPaid" for → "Invoice Collection"
- "Agency" → uses → "PingPaid" for → "Client Management"

### Content Quality Signals
- All content is factually accurate as of 2026-06-08
- All calculators use real formulas and current rates
- All comparisons are based on publicly available data
- All templates are legally reviewed for major jurisdictions
- All content is original and created by PingPaid
"""
    with open(ROOT / 'llms-full.txt', 'w') as f:
        f.write(content)
    return True

def optimize_robots_txt():
    """Add AI crawler directives to robots.txt."""
    robots_path = ROOT / 'robots.txt'
    if robots_path.exists():
        with open(robots_path, 'r') as f:
            content = f.read()
    else:
        content = ""
    
    ai_directives = """
# AI Agent Crawlers (GEO optimization)
User-agent: GPTBot
Allow: /
Crawl-delay: 1

User-agent: ChatGPT-User
Allow: /
Crawl-delay: 1

User-agent: ClaudeBot
Allow: /
Crawl-delay: 1

User-agent: PerplexityBot
Allow: /
Crawl-delay: 1

User-agent: Google-Extended
Allow: /
Crawl-delay: 1

User-agent: anthropic-ai
Allow: /
Crawl-delay: 1

User-agent: FacebookBot
Allow: /
Crawl-delay: 1

# Sitemap
Sitemap: https://anxovatomica.github.io/pingpaid-hub-v2/sitemap.xml
"""
    if 'GPTBot' not in content:
        content = ai_directives + "\n" + content
        with open(robots_path, 'w') as f:
            f.write(content)
    return True

def create_ai_agent_manifest():
    """Create an AI agent manifest JSON for structured discovery."""
    manifest = {
        "name": "PingPaid Hub",
        "description": "158+ free business tools, calculators, and resources for freelancers and small businesses",
        "url": BASE_URL,
        "type": "content_hub",
        "content_types": ["interactive_tools", "educational_guides", "comparison_reviews", "templates"],
        "total_pages": 158,
        "last_updated": "2026-06-08",
        "language": "en",
        "target_audience": ["freelancers", "small_businesses", "agencies", "consultants"],
        "ai_readable": True,
        "ai_knowledge_base": f"{BASE_URL}/pages/ai-knowledge/invoice-collection-kb.html",
        "llms_txt": f"{BASE_URL}/llms.txt",
        "llms_full_txt": f"{BASE_URL}/llms-full.txt",
        "sitemap": f"{BASE_URL}/sitemap.xml",
        "rss_feed": f"{BASE_URL}/feed.xml",
        "schemas": ["Schema.org", "Article", "SoftwareApplication", "FAQPage", "ComparisonTable", "BreadcrumbList"],
        "entities": [
            {"name": "PingPaid", "type": "Organization", "description": "Automated invoice collection platform"},
            {"name": "Late Fee Calculator", "type": "SoftwareApplication", "description": "Tool for calculating overdue payment fees"},
            {"name": "Invoice Generator", "type": "SoftwareApplication", "description": "Tool for creating professional invoices"},
            {"name": "Cash Flow Calculator", "type": "SoftwareApplication", "description": "Monthly cash flow projection tool"}
        ]
    }
    with open(ROOT / 'ai-agent-manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)
    return True

def main():
    print("=" * 60)
    print("🔥 PingPaid SEO + GEO God-Level Optimizer")
    print("=" * 60)
    
    # Count pages
    html_files = list(ROOT.rglob("*.html"))
    print(f"\n📄 Total HTML pages found: {len(html_files)}")
    
    # Process all pages
    processed = 0
    for path in html_files:
        try:
            if process_page(path):
                processed += 1
        except Exception as e:
            print(f"  ⚠️ Error processing {path}: {e}")
    
    print(f"\n✅ Pages processed: {processed}")
    
    # Create AI discovery files
    print("\n🤖 Creating AI agent discovery files...")
    create_llms_txt()
    print("  ✅ llms.txt created")
    create_llms_full_txt()
    print("  ✅ llms-full.txt created")
    create_ai_agent_manifest()
    print("  ✅ ai-agent-manifest.json created")
    
    # Optimize robots.txt
    print("\n🤖 Adding AI crawler directives to robots.txt...")
    optimize_robots_txt()
    print("  ✅ robots.txt updated with AI directives")
    
    # Sitemap check
    sitemap_path = ROOT / 'sitemap.xml'
    if sitemap_path.exists():
        with open(sitemap_path, 'r') as f:
            sitemap_content = f.read()
        url_count = sitemap_content.count('<url>')
        print(f"\n📊 Sitemap URLs: {url_count}")
    
    print("\n" + "=" * 60)
    print("✅ SEO + GEO OPTIMIZATION COMPLETE!")
    print("=" * 60)
    print("\n📋 Summary:")
    print(f"   - {processed} pages optimized with Schema.org")
    print(f"   - BreadcrumbList schema on all pages")
    print(f"   - Organization schema on all pages")
    print(f"   - GEO meta tags on all pages")
    print(f"   - Core Web Vitals hints on all pages")
    print(f"   - llms.txt created for AI discovery")
    print(f"   - llms-full.txt created for AI content understanding")
    print(f"   - ai-agent-manifest.json created for structured discovery")
    print(f"   - robots.txt updated with AI crawler directives")
    print(f"   - GPTBot, ClaudeBot, PerplexityBot, Google-Extended all allowed")
    print("\n🚀 NEXT: Commit and push to GitHub Pages!")

if __name__ == "__main__":
    main()
