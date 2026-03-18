import requests
from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin, urlparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_internal_links(url):
    try:
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')

        base_domain = urlparse(url).netloc
        internal_links = set()

        for a_tag in soup.find_all('a'):
            href = a_tag.get('href')

            if href:
                full_url = urljoin(url, href)
                parsed_url = urlparse(full_url)

                # keep only internal links
                if parsed_url.netloc == base_domain:
                    internal_links.add(full_url)

        return list(internal_links)

    except Exception as e:
        print("Error:", e)
        return []

def check_link_status(links):
    healthy = []
    redirect = []
    broken = []

    for link in links:
        try:
            response = requests.get(link, verify=False, timeout=5)
            status = response.status_code

            if status == 200:
                healthy.append(link)
            elif 300 <= status < 400:
                redirect.append(link)
            else:
                broken.append(link)

        except Exception:
            broken.append(link)

    return healthy, redirect, broken

if __name__ == "__main__":
    url = "https://books.toscrape.com"

    print(f"\n🔍 Scanning: {url}\n")

    links = get_internal_links(url)

    print(f"Total internal links found: {len(links)}")

    healthy, redirect, broken = check_link_status(links)

    print("\n" + "="*50)
    print("✅ HEALTHY LINKS")
    print("="*50)
    for link in healthy:
        print(link)

    print("\n" + "="*50)
    print("🔁 REDIRECTING LINKS")
    print("="*50)
    for link in redirect:
        print(link)

    print("\n" + "="*50)
    print("❌ BROKEN LINKS")
    print("="*50)
    for link in broken:
        print(link)

    print("\n" + "="*50)
    print("📊 SUMMARY")
    print("="*50)
    print(f"Healthy: {len(healthy)}")
    print(f"Redirecting: {len(redirect)}")
    print(f"Broken: {len(broken)}")