import requests
from urllib.parse import urlparse, urljoin, urlunparse
from bs4 import BeautifulSoup

class BlogUrlFinder:
    def __init__(self, base_url):
        self.base_urls = self._prepare_url_variants(base_url)

    def _prepare_url_variants(self, user_input):
        """Normalize the user input URL and prepare www and non-www variants."""
        parsed = urlparse(user_input, 'https')
        if not parsed.netloc:
            parsed = urlparse('https://' + user_input)
        base = parsed.netloc
        www_variant = 'www.' + base if not base.startswith('www.') else base
        non_www_variant = base[4:] if base.startswith('www.') else base
        schemes = ['http', 'https']
        return [urlunparse((scheme, variant, parsed.path, parsed.params, parsed.query, parsed.fragment))
                for variant in (base, www_variant, non_www_variant) for scheme in schemes]

    def find_sitemap_url(self):
        """Try common sitemap URLs and check robots.txt for both www and non-www variants."""
        common_paths = ['sitemap.xml', 'sitemap_index.xml', 'sitemap-index.xml', 'sitemap1.xml']
        for base_url in self.base_urls:
            for path in common_paths:
                sitemap_url = urljoin(base_url, path)
                if self._url_exists(sitemap_url):
                    return sitemap_url
            robots_url = urljoin(base_url, 'robots.txt')
            sitemap_from_robots = self._find_sitemap_from_robots_txt(robots_url)
            if sitemap_from_robots:
                return sitemap_from_robots
        return None

    def _url_exists(self, url):
        """Check if the URL exists by making a HEAD request."""
        try:
            response = requests.head(url)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def _find_sitemap_from_robots_txt(self, robots_url):
        """Attempt to find a sitemap URL in the robots.txt file."""
        try:
            response = requests.get(robots_url)
            for line in response.text.splitlines():
                if line.startswith('Sitemap:'):
                    return line.split(': ')[1].strip()
        except requests.RequestException:
            return None

    def fetch_blog_urls(self, sitemap_url=None):
        """Fetch blog post URLs from a sitemap or attempt to scrape the site directly if no sitemap is found."""
        if not sitemap_url:
            sitemap_url = self.find_sitemap_url()
        if sitemap_url:
            urls = self._fetch_urls_from_sitemap(sitemap_url)
        else:
            # Fallback: Attempt to scrape the main page or blog index for blog post URLs
            urls = self._attempt_scrape_site_for_blog_urls()
        return list(set(urls))  # Convert to set and back to list to remove duplicates

    def _fetch_urls_from_sitemap(self, sitemap_url):
        """Recursively fetch URLs from a sitemap, including nested sitemaps."""
        urls = []
        response = requests.get(sitemap_url)
        soup = BeautifulSoup(response.content, 'xml')
        for sitemap in soup.find_all('sitemap'):
            nested_sitemap_url = sitemap.find('loc').text
            urls.extend(self._fetch_urls_from_sitemap(nested_sitemap_url))
        for url in soup.find_all('url'):
            loc = url.find('loc').text
            if self._is_blog_post_url(loc):
                urls.append(loc)
        return urls

    def _is_blog_post_url(self, url):
        """Determine if a URL is likely a blog post and not a tag/category page."""
        excluded_patterns = ['tag', 'category', 'author', 'page', 'comment', 'archive', 'login', 'search', '#', '?']
        return not any(pattern in url for pattern in excluded_patterns)

    def _attempt_scrape_site_for_blog_urls(self):
        """Fallback method to scrape the main blog page for blog post URLs."""
        blog_urls = []
        for base_url in self.base_urls:
            try:
                response = requests.get(base_url)
                soup = BeautifulSoup(response.content, 'html.parser')
                links = [a['href'] for a in soup.find_all('a', href=True) if self._is_blog_post_url(a['href'])]
                blog_urls.extend(links)
            except requests.RequestException:
                continue
        return list(set(blog_urls))  # Remove duplicates and return
    
if __name__ == "__main__":
    # Example Usage:
    base_url = "https://www.dynamikapps.com"  # Replace with the actual website URL to test
    finder = BlogUrlFinder(base_url)
    sitemap_url = finder.find_sitemap_url()
    if sitemap_url:
        print(f"Sitemap found at: {sitemap_url}")
        blog_post_urls = finder.fetch_blog_urls(sitemap_url)
        for url in blog_post_urls:
            print(url)
    else:
        print("Sitemap not found. Attempting to scrape site for blog URLs...")
        blog_post_urls = finder.fetch_blog_urls()  # Attempt scraping if no sitemap
        for url in blog_post_urls:
            print(url)
