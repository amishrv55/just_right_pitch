# proposals/utils.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

def fetch_job_description(url):
    """
    Fetches job description text from a LinkedIn or Upwork job URL.
    Returns: (description_text, error_message_or_None)
    """
    try:
        domain = urlparse(url).netloc.lower()

        # LinkedIn scraping (fast)
        if "linkedin.com" in domain:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/115.0 Safari/537.36"
            }
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code != 200:
                return None, f"LinkedIn fetch failed (status {resp.status_code})."

            soup = BeautifulSoup(resp.text, "html.parser")
            job_desc_elem = soup.find("div", class_="show-more-less-html__markup")
            if not job_desc_elem:
                return None, "LinkedIn description not found."

            text = job_desc_elem.get_text("\n", strip=True)
            return text, None

        # Upwork scraping (needs JS execution)
        elif "upwork.com" in domain:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=60000)
                page.wait_for_selector("h1.m-0.h4", timeout=20000)  # Wait for title

                title = page.query_selector("h1.m-0.h4")
                description = page.query_selector("p.text-body-sm")

                title_text = title.inner_text().strip() if title else ""
                description_text = description.inner_text().strip() if description else ""

                browser.close()

                if not description_text:
                    return None, "Upwork description not found."

                return f"{title_text}\n\n{description_text}", None

        else:
            return None, "Unsupported platform URL."

    except Exception as e:
        return None, str(e)


