#!/usr/bin/env python3
"""Add extra GEO optimizations to all HTML pages in PingPaid Hub."""

import glob
import os
import re

BASE_DIR = "/root/.openclaw/workspace/pingpaid-hub-v2"
AI_KB_URL = "https://anxovatomica.github.io/pingpaid-hub-v2/pages/ai-knowledge/invoice-collection-kb.html"

def add_rel_help(html_content):
    """Add rel='help' link to AI knowledge base in <head>."""
    # Check if already present
    if 'rel="help"' in html_content:
        return html_content
    
    # Insert after the canonical link or before </head>
    help_link = f'<link rel="help" href="{AI_KB_URL}" title="AI Knowledge Base for Invoice Collection" />\n'
    
    # Try to insert after canonical link
    if '<link rel="canonical"' in html_content:
        html_content = re.sub(
            r'(<link rel="canonical"[^>]*>\n?)',
            r'\1\n' + help_link,
            html_content,
            count=1
        )
    else:
        # Insert before </head>
        html_content = html_content.replace('</head>', help_link + '</head>')
    
    return html_content

def add_data_ai_purpose(html_content):
    """Add data-ai-purpose attributes to key content sections."""
    
    # Map of patterns to replacements
    replacements = [
        # Container divs
        (r'<div class="container">', '<div class="container" data-ai-purpose="main-content" itemscope itemtype="https://schema.org/WebPage">'),
        
        # Header
        (r'<header(\s*[^>]*)>', r'<header\1 data-ai-purpose="page-header" itemscope itemtype="https://schema.org/WPHeader">'),
        
        # Footer
        (r'<footer(\s*[^>]*)>', r'<footer\1 data-ai-purpose="page-footer" itemscope itemtype="https://schema.org/WPFooter">'),
        
        # Tools grid
        (r'<div class="tools-grid">', '<div class="tools-grid" data-ai-purpose="tools-directory">'),
        
        # Tool cards (only if not already modified)
        (r'<a class="tool-card"', '<a class="tool-card" data-ai-purpose="tool-card" itemscope itemtype="https://schema.org/SoftwareApplication"'),
        
        # CTA section
        (r'<div class="cta-section">', '<div class="cta-section" data-ai-purpose="call-to-action">'),
        
        # Stats section
        (r'<div class="stats">', '<div class="stats" data-ai-purpose="statistics">'),
        
        # Featured section
        (r'<div class="featured">', '<div class="featured" data-ai-purpose="featured-content">'),
        
        # Testimonial
        (r'<div class="testimonial">', '<div class="testimonial" data-ai-purpose="testimonial" itemscope itemtype="https://schema.org/Review">'),
        
        # Blog content (for blog pages)
        (r'<div class="content">', '<div class="content" data-ai-purpose="article-body" itemscope itemtype="https://schema.org/Article">'),
        
        # Article tags
        (r'<article(\s*[^>]*)>', r'<article\1 data-ai-purpose="article-content" itemscope itemtype="https://schema.org/Article">'),
    ]
    
    for pattern, replacement in replacements:
        # Only replace if the attribute isn't already there
        if 'data-ai-purpose' not in pattern or not re.search(r'data-ai-purpose', html_content):
            html_content = re.sub(pattern, replacement, html_content, count=0)
    
    return html_content

def process_page(filepath):
    """Process a single HTML page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    content = add_rel_help(content)
    content = add_data_ai_purpose(content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    html_files = glob.glob(os.path.join(BASE_DIR, "**/*.html"), recursive=True)
    modified = 0
    
    for filepath in html_files:
        if process_page(filepath):
            modified += 1
            print(f"  ✅ {os.path.relpath(filepath, BASE_DIR)}")
    
    print(f"\n🎯 Modified {modified}/{len(html_files)} pages with extra GEO optimizations")

if __name__ == "__main__":
    main()
