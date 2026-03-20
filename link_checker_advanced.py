import requests
from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
import sys
import csv
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# extract internal links
def get_internal_links(url):
    try:
        response = requests.get(url, verify=False, timeout=5, allow_redirects=False) #try with 20 and check RAM usage
        soup = BeautifulSoup(response.text, 'html.parser')

        base_domain = urlparse(url).netloc
        internal_links = set()

        for a_tag in soup.find_all('a'):
            href = a_tag.get('href')

            if href:
                full_url = urljoin(url, href)
                parsed_url = urlparse(full_url)

                if parsed_url.netloc == base_domain:
                    internal_links.add(full_url)

        return list(internal_links)

    except Exception as e:
        print("Error fetching page:", e)
        return []

# Check single link (for threading)
def check_single_link(link):
    try:
        response = requests.get(link, verify=False, timeout=5, allow_redirects=False)
        status_code = response.status_code

        if response.is_redirect or response.status_code in [301, 302, 303, 307, 308]:  # Redirect via status code or loc header
            return link, status_code, "redirect"

        elif response.status_code == 200:
            return link, status_code, "healthy"

        else:
            return link, status_code, "broken"

    except:
        return link, status_code, "broken"

# Parallel link checking with status code
def check_link_status(links):
    healthy, redirect, broken = [], [], []

    healthy_data, redirect_data, broken_data = [], [], []

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(check_single_link, links))

    for link, status_code, category in results:

        if category == "healthy":
            healthy.append(link)
            healthy_data.append((link, status_code))

        elif category == "redirect":
            redirect.append(link)
            redirect_data.append((link, status_code))

        else:
            broken.append(link)
            broken_data.append((link, status_code))

    return healthy, redirect, broken, healthy_data, redirect_data, broken_data

# Export to CSV
def export_to_csv(healthy, redirect, broken):
    with open("report.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Type", "URL"])

        for link in healthy:
            writer.writerow(["Healthy", link])
        for link in redirect:
            writer.writerow(["Redirect", link])
        for link in broken:
            writer.writerow(["Broken", link])

    print("\n Report saved as report.csv")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python link_checker_advanced.py <URL>")
        sys.exit(1)

    url = sys.argv[1]

    start_time = time.time()

    print(f"\n Scanning: {url}\n")

    links = get_internal_links(url)

    print(f"Total internal links found: {len(links)}")

    healthy, redirect, broken, _, _, _ = check_link_status(links)

    print("\n" + "=" * 50)
    print(" HEALTHY LINKS")
    print("=" * 50)
    for link in healthy:
        print(link)

    print("\n" + "=" * 50)
    print(" REDIRECTING LINKS")
    print("=" * 50)
    for link in redirect:
        print(link)

    print("\n" + "=" * 50)
    print(" BROKEN LINKS")
    print("=" * 50)
    for link in broken:
        print(link)

    print("\n" + "=" * 50)
    print(" SUMMARY")
    print("=" * 50)
    print(f"Healthy: {len(healthy)}")
    print(f"Redirecting: {len(redirect)}")
    print(f"Broken: {len(broken)}")

    # Export results
    export_to_csv(healthy, redirect, broken)

    end_time = time.time()
    print(f"\n Execution Time: {round(end_time - start_time, 2)} seconds\n")