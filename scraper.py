import requests
from bs4 import BeautifulSoup

def extract_article(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        for tag in soup(['script', 'style', 'header', 'footer', 'nav']):
            tag.decompose()

        title_tag = soup.find(['h1', 'title'])
        title = title_tag.get_text(strip=True) if title_tag else ""

        paragraphs = soup.find_all("p")
        content = " ".join([p.get_text(strip=True) for p in paragraphs])

        return f"{title}\n\n{content}".strip()  # ✅ return as a single string
    except Exception as e:
        print(f"[ERROR extracting article] {url}: {e}")
        return ""
