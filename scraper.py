import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()

# Configuración mínima: usa Tor si está en 127.0.0.1:9050
PROXY = "socks5h://127.0.0.1:9050"

proxies = {"http": PROXY, "https": PROXY} if PROXY else None

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; scraper/1.0)"})
if proxies:
    session.proxies.update(proxies)

# URL objetivo (Wikipedia)
url = "https://es.wikipedia.org/wiki/Real_Madrid_Club_de_F%C3%BAtbol"

def get_ip_and_country(sess):
    try:
        r = sess.get('https://ipwhois.app/json', timeout=10)
        r.raise_for_status()
        data = r.json()
        ip = data.get('ip')
        country = data.get('country') or data.get('country_code')
        return ip, country
    except Exception:
        return None, None

def get_title(sess, url):
    r = sess.get(url, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    # Wikipedia usa #firstHeading para el título principal
    h = soup.select_one('#firstHeading')
    if h and h.get_text(strip=True):
        return h.get_text(strip=True)
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return None

def print_result(ip, country, title):
    # salida 'pro' usando rich
    meta = Table.grid(expand=True)
    meta.add_column(justify="left")
    meta.add_column(justify="right")
    meta.add_row("Modo:", PROXY and "Tor (socks5)" or "Directo")
    meta.add_row("Timestamp:", datetime.now(timezone.utc).isoformat())

    data = Table.grid(padding=(0, 2))
    data.add_column(style="bold cyan", justify="right")
    data.add_column(style="")
    data.add_row("IP", f"[cyan]{ip or 'N/A'}")
    data.add_row("País", f"[green]{country or 'N/A'}")
    data.add_row("Título", f"[magenta]{title or 'N/D'}")

    inner = Table.grid()
    inner.add_row(Panel(meta, box=box.SQUARE, padding=(0,1)))
    inner.add_row(Panel(data, title="Resultado", box=box.ROUNDED, padding=(1,2)))

    panel = Panel.fit(
        inner,
        title="Scraper Profesional",
        subtitle="Salida limpia y lista para informes",
        box=box.DOUBLE,
    )

    console.print(panel)


def main():
    ip, country = get_ip_and_country(session)
    try:
        title = get_title(session, url)
    except Exception as e:
        title = None
    print_result(ip, country, title)


if __name__ == '__main__':
    main()