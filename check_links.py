#!/usr/bin/env python3
"""
Comprehensive internal link checker for Hugo site.
Extracts all internal links from generated HTML and validates them.
"""

import os
import re
from pathlib import Path
from urllib.parse import urlparse, urljoin
from collections import defaultdict
import json

class LinkChecker:
    def __init__(self, public_dir='public'):
        self.public_dir = Path(public_dir)
        self.all_links = defaultdict(set)  # source_file -> set of links
        self.all_pages = set()  # all valid page paths
        self.broken_links = []  # list of broken link info

    def find_all_html_files(self):
        """Find all HTML files in the public directory."""
        return list(self.public_dir.rglob('*.html'))

    def normalize_path(self, path):
        """Normalize a path for comparison."""
        # Remove leading/trailing slashes
        path = path.strip('/')
        # Remove index.html
        path = re.sub(r'/index\.html$', '', path)
        path = re.sub(r'^index\.html$', '', path)
        return path

    def extract_internal_links(self, html_file):
        """Extract all internal links from an HTML file."""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {html_file}: {e}")
            return []

        # Find all href attributes
        href_pattern = r'href=["\']([^"\']+)["\']'
        links = re.findall(href_pattern, content)

        internal_links = []
        for link in links:
            # Skip external links, mailto, tel, javascript, anchors
            if any(link.startswith(prefix) for prefix in ['http://', 'https://', 'mailto:', 'tel:', 'javascript:', '//']):
                continue
            if link.startswith('#'):
                continue
            if link == '':
                continue

            # This is an internal link
            internal_links.append(link)

        return internal_links

    def get_page_path(self, html_file):
        """Convert HTML file path to URL path."""
        rel_path = html_file.relative_to(self.public_dir)
        # Convert to string and normalize
        path_str = str(rel_path)
        # Remove index.html
        path_str = path_str.replace('/index.html', '/')
        path_str = path_str.replace('index.html', '/')
        # Ensure starts with /
        if not path_str.startswith('/'):
            path_str = '/' + path_str
        return path_str

    def build_page_inventory(self):
        """Build inventory of all valid pages."""
        html_files = self.find_all_html_files()

        for html_file in html_files:
            # Add the file itself
            page_path = self.get_page_path(html_file)
            self.all_pages.add(page_path)

            # Also add without trailing slash
            if page_path.endswith('/') and page_path != '/':
                self.all_pages.add(page_path.rstrip('/'))

            # Also add with trailing slash
            if not page_path.endswith('/'):
                self.all_pages.add(page_path + '/')

            # Add the actual file path
            rel_path = html_file.relative_to(self.public_dir)
            file_path = '/' + str(rel_path)
            self.all_pages.add(file_path)

    def link_exists(self, link):
        """Check if a link target exists."""
        # Normalize the link
        link = link.split('#')[0]  # Remove anchor
        link = link.split('?')[0]  # Remove query string

        if not link or link == '/':
            return True

        # Check various forms
        checks = [
            link,
            link + '/',
            link.rstrip('/'),
            link + '/index.html',
            link.rstrip('/') + '/index.html'
        ]

        for check in checks:
            if check in self.all_pages:
                return True

            # Also check if the file exists
            if check.startswith('/'):
                file_path = self.public_dir / check.lstrip('/')
                if file_path.exists():
                    return True

        return False

    def check_all_links(self):
        """Check all links in all HTML files."""
        html_files = self.find_all_html_files()

        print(f"Found {len(html_files)} HTML files")
        print(f"Found {len(self.all_pages)} valid page paths")
        print("\nChecking links...\n")

        total_links = 0

        for html_file in html_files:
            source_path = self.get_page_path(html_file)
            links = self.extract_internal_links(html_file)

            for link in links:
                total_links += 1
                self.all_links[source_path].add(link)

                if not self.link_exists(link):
                    self.broken_links.append({
                        'source': source_path,
                        'broken_link': link,
                        'source_file': str(html_file)
                    })

        print(f"Total internal links checked: {total_links}")
        print(f"Broken links found: {len(self.broken_links)}")

        return self.broken_links

    def suggest_fix(self, broken_link):
        """Suggest a fix for a broken link."""
        # Common patterns
        suggestions = []

        # Check if it's a language prefix issue
        if broken_link.startswith('/en/'):
            without_lang = broken_link.replace('/en/', '/', 1)
            if self.link_exists(without_lang):
                suggestions.append(without_lang)

        # Check common redirects
        redirects = {
            '/contact': '/business/contact/',
            '/demo': '/business/demo/',
            '/docs': '/get-started/',
            '/api': '/technical/api/',
            '/community': '/business/community/',
            '/about': '/business/about/',
            '/pricing': '/business/pricing/',
        }

        for old, new in redirects.items():
            if broken_link == old or broken_link == old + '/':
                if self.link_exists(new):
                    suggestions.append(new)

        # Try to find similar pages
        link_parts = broken_link.strip('/').split('/')
        if link_parts:
            last_part = link_parts[-1]
            for page in self.all_pages:
                if last_part in page:
                    suggestions.append(page)
                    if len(suggestions) >= 3:
                        break

        return suggestions[:3] if suggestions else ["Unable to suggest fix"]

    def generate_report(self):
        """Generate a comprehensive report of broken links."""
        report = []

        report.append("# Broken Links Report\n")
        report.append(f"**Total HTML files analyzed:** {len(self.find_all_html_files())}")
        report.append(f"**Total valid pages found:** {len(self.all_pages)}")
        report.append(f"**Total internal links checked:** {sum(len(links) for links in self.all_links.values())}")
        report.append(f"**Broken links found:** {len(self.broken_links)}\n")

        if not self.broken_links:
            report.append("✅ **No broken links found!**\n")
            return '\n'.join(report)

        # Group by broken link
        by_link = defaultdict(list)
        for item in self.broken_links:
            by_link[item['broken_link']].append(item['source'])

        report.append("## Broken Links Details\n")

        for broken_link, sources in sorted(by_link.items()):
            report.append(f"### `{broken_link}`")
            report.append(f"**Found on {len(sources)} page(s):**")
            for source in sorted(set(sources))[:10]:  # Show first 10
                report.append(f"- {source}")
            if len(sources) > 10:
                report.append(f"- ... and {len(sources) - 10} more pages")

            suggestions = self.suggest_fix(broken_link)
            report.append(f"\n**Suggested fix:** {suggestions[0]}")
            if len(suggestions) > 1:
                report.append("**Other suggestions:**")
                for sugg in suggestions[1:]:
                    report.append(f"- {sugg}")
            report.append("")

        # Common patterns
        report.append("\n## Common Broken Link Patterns\n")
        patterns = defaultdict(int)
        for broken_link in by_link.keys():
            if broken_link.startswith('/contact'):
                patterns['/contact* → Should be /business/contact/'] += len(by_link[broken_link])
            elif broken_link.startswith('/demo'):
                patterns['/demo* → Should be /business/demo/'] += len(by_link[broken_link])
            elif broken_link.startswith('/docs'):
                patterns['/docs* → Should be /get-started/ or /technical/'] += len(by_link[broken_link])
            elif broken_link.startswith('/api'):
                patterns['/api* → Should be /technical/api/'] += len(by_link[broken_link])
            elif broken_link.startswith('/community'):
                patterns['/community* → Should be /business/community/'] += len(by_link[broken_link])

        for pattern, count in sorted(patterns.items(), key=lambda x: x[1], reverse=True):
            report.append(f"- {pattern} ({count} occurrences)")

        return '\n'.join(report)

if __name__ == '__main__':
    import sys
    public_dir = sys.argv[1] if len(sys.argv) > 1 else 'public'
    checker = LinkChecker(public_dir)

    print("Building page inventory...")
    checker.build_page_inventory()

    print("\nChecking all links...")
    broken_links = checker.check_all_links()

    print("\n" + "="*80)
    report = checker.generate_report()
    print(report)

    # Save to file
    with open('broken_links_report.md', 'w') as f:
        f.write(report)

    print("\n" + "="*80)
    print(f"\nReport saved to: broken_links_report.md")
