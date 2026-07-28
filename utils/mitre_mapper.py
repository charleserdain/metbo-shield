def map_mitre(findings: list[dict]) -> list[dict]:
    mappings = {}
    for finding in findings:
        category = finding.get("category", "")
        evidence = finding.get("evidence", "").lower()
        if category in {"Language","Sender","Authentication"}:
            mappings["T1566"] = {"Technique":"T1566","Name":"Phishing","Reason":"Social-engineering or sender-deception indicators were detected."}
        if category == "URL":
            mappings["T1566.002"] = {"Technique":"T1566.002","Name":"Spearphishing Link","Reason":"A suspicious or mismatched URL was detected."}
        if category == "Attachment":
            mappings["T1566.001"] = {"Technique":"T1566.001","Name":"Spearphishing Attachment","Reason":"A potentially dangerous attachment was detected."}
        if "verify your account" in evidence or "confirm your identity" in evidence:
            mappings["T1056"] = {"Technique":"T1056","Name":"Input Capture","Reason":"The lure may attempt to collect credentials."}
    return list(mappings.values())
