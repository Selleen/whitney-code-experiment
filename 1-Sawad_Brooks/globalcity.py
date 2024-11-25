import requests
from bs4 import BeautifulSoup

def fetch_web_content(url):
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()  # Lanza una excepción para errores HTTP
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.prettify()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return f"<p>Error fetching {url}: {e}</p>"

# Sitios de prueba
urls = ["http://www.nytimes.com", "http://www.theguardian.com/uk", "http://www.asahi.com"]

with open("global.html", "w", encoding="utf-8") as file:
    for i, url in enumerate(urls):
        content = fetch_web_content(url)
        file.write(f'<div style="position: absolute; left: {i * 200}px; top: 0px;">')
        file.write(content)
        file.write("</div>")
