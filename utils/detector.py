from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import urlparse
from .helpers import email_domain, auth_result, threat_level, classification
from .ioc_extractor import extract_iocs

SUSPICIOUS_PHRASES = {
    "verify your account": 18,
    "urgent action required": 16,
    "password expires": 16,
    "click immediately": 14,
    "confirm your identity": 18,
    "unusual activity": 12,
    "wire transfer": 18,
    "gift card": 16,
}
DANGEROUS_EXTENSIONS = {".exe",".scr",".js",".vbs",".bat",".cmd",".iso",".img",".lnk",".docm",".xlsm"}
SHORTENERS = {"bit.ly","tinyurl.com","t.co","goo.gl","ow.ly","is.gd"}
RISKY_TLDS = {".zip",".mov",".click",".top",".xyz",".work",".support"}

@dataclass
class Finding:
    category: str
    severity: str
    evidence: str
    points: int

def analyze_email(email: dict) -> dict:
    findings = []
    subject = email.get("subject", "")
    body = email.get("body", "")
    text = f"{subject}\n{body}".lower()
    sender_domain = email_domain(email.get("from", ""))
    reply_domain = email_domain(email.get("reply_to", ""))
    iocs = extract_iocs("\n".join([subject, body, email.get("from",""), email.get("reply_to","")]))

    for phrase, points in SUSPICIOUS_PHRASES.items():
        if phrase in text:
            findings.append(Finding("Language", "High" if points >= 16 else "Medium", f'Suspicious phrase: "{phrase}"', points))

    if sender_domain and reply_domain and sender_domain != reply_domain:
        findings.append(Finding("Sender", "High", f"Reply-To domain {reply_domain} differs from sender domain {sender_domain}", 22))

    for attachment in email.get("attachments", []):
        if Path(attachment.lower()).suffix in DANGEROUS_EXTENSIONS:
            findings.append(Finding("Attachment", "Critical", f"Potentially dangerous attachment: {attachment}", 30))

    for url in iocs["urls"]:
        domain = (urlparse(url).hostname or "").lower().removeprefix("www.")
        if domain in SHORTENERS:
            findings.append(Finding("URL", "High", f"URL shortener detected: {domain}", 18))
        if any(domain.endswith(tld) for tld in RISKY_TLDS):
            findings.append(Finding("URL", "High", f"Risky top-level domain: {domain}", 16))
        if sender_domain and domain and sender_domain not in domain:
            findings.append(Finding("URL", "Medium", f"Linked domain differs from sender domain: {domain}", 8))

    headers = email.get("headers", {})
    authentication = {name.upper(): auth_result(headers, name) for name in ("spf","dkim","dmarc")}
    for protocol, result in authentication.items():
        if result in {"fail","softfail"}:
            findings.append(Finding("Authentication", "High", f"{protocol} result: {result}", 18))
        elif result in {"none","unknown"}:
            findings.append(Finding("Authentication", "Low", f"{protocol} result unavailable", 3))

    finding_dicts = [asdict(x) for x in findings]
    score = min(100, sum(x["points"] for x in finding_dicts))
    return {
        "rule_score": score,
        "classification": classification(score),
        "threat_level": threat_level(score),
        "findings": finding_dicts,
        "iocs": iocs,
        "sender_domain": sender_domain,
        "reply_to_domain": reply_domain,
        "authentication": authentication,
    }
