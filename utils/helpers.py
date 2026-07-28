from email.utils import parseaddr

def email_domain(value: str) -> str:
    address = parseaddr(value or "")[1]
    return address.rsplit("@", 1)[-1].lower() if "@" in address else ""

def auth_result(headers: dict, token: str) -> str:
    text = " ".join([
        headers.get("authentication-results", ""),
        headers.get("received-spf", ""),
    ]).lower()
    for result in ("pass", "fail", "softfail", "neutral", "none"):
        if f"{token}={result}" in text:
            return result
    return "unknown"

def threat_level(score: int) -> str:
    if score >= 85: return "Critical"
    if score >= 65: return "High"
    if score >= 40: return "Medium"
    if score >= 20: return "Low"
    return "Informational"

def classification(score: int) -> str:
    if score >= 65: return "Likely Phishing"
    if score >= 35: return "Suspicious"
    return "Low Apparent Risk"

def recommendation(score: int) -> str:
    if score >= 85:
        return "Quarantine the message, block observed IOCs, and escalate immediately."
    if score >= 65:
        return "Quarantine the message and escalate for analyst validation."
    if score >= 35:
        return "Hold the message and verify the sender through an independent channel."
    return "No immediate containment action is indicated. Continue standard caution."
