import base64, requests
BASE_URL = "https://www.virustotal.com/api/v3"

def lookup(indicator: str, indicator_type: str, api_key: str) -> dict:
    if not api_key:
        return {"error":"VirusTotal API key is not configured."}
    if indicator_type == "url":
        url_id = base64.urlsafe_b64encode(indicator.encode()).decode().strip("=")
        endpoint = f"{BASE_URL}/urls/{url_id}"
    elif indicator_type == "domain":
        endpoint = f"{BASE_URL}/domains/{indicator}"
    elif indicator_type == "ip":
        endpoint = f"{BASE_URL}/ip_addresses/{indicator}"
    else:
        return {"error":"Unsupported indicator type."}
    try:
        response = requests.get(endpoint, headers={"x-apikey":api_key}, timeout=15)
        if response.status_code == 401: return {"error":"VirusTotal rejected the API key."}
        if response.status_code == 404: return {"error":"Indicator not found."}
        if response.status_code == 429: return {"error":"VirusTotal rate limit reached."}
        response.raise_for_status()
        stats = response.json()["data"]["attributes"].get("last_analysis_stats",{})
        return {
            "malicious":stats.get("malicious",0),
            "suspicious":stats.get("suspicious",0),
            "harmless":stats.get("harmless",0),
            "undetected":stats.get("undetected",0),
        }
    except requests.RequestException as exc:
        return {"error":f"VirusTotal request failed: {exc}"}
