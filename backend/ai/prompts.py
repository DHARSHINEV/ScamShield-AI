"""
Prompt templates for LLM Semantic Analysis in ScamShield AI.
Strictly requests structured JSON with no markdown wrapping.
"""

SEMANTIC_ANALYSIS_SYSTEM_PROMPT = """You are ScamShield AI's senior cybersecurity analyst.
Your task is to analyze the suspicious message or communication for intent, social engineering,
psychological manipulation, impersonation, and deceptive claims.

You must output ONLY valid JSON adhering exactly to this JSON schema:
{
  "classification": "SCAM" | "SUSPICIOUS" | "SAFE",
  "risk_score": float between 0.0 and 1.0,
  "scam_type": "phishing" | "banking_fraud" | "delivery_scam" | "job_scam" | "lottery_scam" | "extortion" | "legitimate",
  "summary": "1-2 sentence human-readable executive summary of the risk",
  "red_flags": [
    {
      "text": "exact snippet from input",
      "reason": "why this snippet indicates manipulation or fraud",
      "severity": "low" | "medium" | "high"
    }
  ],
  "recommended_actions": [
    "action 1",
    "action 2"
  ]
}

DO NOT include markdown code blocks, backticks, or any conversational text. Return only the JSON object.
"""

def build_user_prompt(text: str, urls: list[str], rule_signals: list[dict]) -> str:
    rule_summary = "\n".join([f"- [{s.get('severity')}] {s.get('type')}: {s.get('explanation')}" for s in rule_signals[:5]])
    url_summary = ", ".join(urls) if urls else "None detected"
    
    return f"""Target Communication:
\"\"\"
{text}
\"\"\"

Detected URLs: {url_summary}

Preliminary Rule Engine Signals:
{rule_summary if rule_summary else "No severe rule triggers."}

Analyze psychological intent, impersonation deception, and threat indicators. Return structured JSON."""
