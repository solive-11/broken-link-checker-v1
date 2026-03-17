#  Broken Link Checker

A Python-based tool that crawls a given website URL, extracts all internal links (one level deep), and checks their HTTP status to identify broken and redirecting links.

---

##  Features

- Extracts all anchor (`<a>`) links from a webpage
- Converts relative URLs to absolute URLs
- Filters only internal links (same domain)
- Checks HTTP status of each link
- Categorizes links into:
  - ✅ Healthy (200 OK)
  - 🔁 Redirecting (3xx)
  - ❌ Broken (4xx, 5xx)
- Displays a clean structured report

---

##  Tech Stack

- Python
- requests
- BeautifulSoup (bs4)

---

##  Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/broken-link-checker.git
cd broken-link-checker

### 2. Install dependencies

```bash
pip install -r requirements.txt

▶️ Usage

Run the script:
python link_checker.py

Modify the target URL inside the script:
url = "https://books.toscrape.com"

⚠️ Notes

SSL verification is disabled for development purposes.
In production environments, SSL verification should always be enabled.
The crawler is limited to one level deep (non-recursive), as per requirements.

📌 Future Improvements

Accept URL as a command-line argument
Export results to CSV or JSON
Add recursive crawling
Include external link checking
Add response time metrics

Author: S Olive Keran