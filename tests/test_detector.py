from utils.detector import analyze_email

def test_phishing_scores_high():
    result = analyze_email({
        "from":"Security <security@fake.xyz>",
        "reply_to":"help@different.click",
        "subject":"Urgent action required",
        "body":"Verify your account. Click immediately: https://bit.ly/test",
        "attachments":[],
        "headers":{"authentication-results":"spf=fail dkim=fail dmarc=fail"},
    })
    assert result["rule_score"] >= 65
    assert result["classification"] == "Likely Phishing"

def test_legitimate_scores_low():
    result = analyze_email({
        "from":"Support <support@example.com>",
        "reply_to":"",
        "subject":"Maintenance completed",
        "body":"No action is required.",
        "attachments":[],
        "headers":{"authentication-results":"spf=pass dkim=pass dmarc=pass"},
    })
    assert result["rule_score"] < 35
