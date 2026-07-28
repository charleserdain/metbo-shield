import re
from urllib.parse import urlparse

URL_RE = re.compile(r'https?://[^\s<>"\']+', re.I)
IP_RE = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
EMAIL_RE = re.compile(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', re.I)

def extract_iocs(text: str) -> dict:
    urls = sorted(set(x.rstrip(".,);]") for x in URL_RE.findall(text or "")))
    emails = sorted(set(EMAIL_RE.findall(text or "")))
    ips = sorted({
        ip for ip in IP_RE.findall(text or "")
        if all(0 <= int(part) <= 255 for part in ip.split("."))
    })
    domains = set()
    for url in urls:
        try:
            host = (urlparse(url).hostname or "").lower()
            if host:
                domains.add(host)
        except ValueError:
            pass
    for address in emails:
        domains.add(address.split("@", 1)[1].lower())
    return {"urls": urls, "domains": sorted(domains), "ips": ips, "emails": emails}
