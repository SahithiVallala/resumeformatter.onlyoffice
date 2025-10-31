# DeepSeek Integration Guide for RF.TS (Resume Formatter)

This guide explains if you should integrate DeepSeek, when it’s beneficial, how to integrate it into your Flask backend and React frontend, what it costs, and trade‑offs to consider.

---

## Executive Summary

- **Is it needed?** Not strictly required for RF.TS to function. Your current pipeline is deterministic and fast. DeepSeek is a high‑impact optional enhancement for better parsing, classification, rewriting, and filling gaps in messy resumes.
- **When it helps most**
  - **Parsing robustness** for noisy/scanned PDFs and unconventional formats.
  - **Skills extraction & normalization** beyond rule-based logic.
  - **Summarization & rewriting** of bullets into ATS‑friendly phrasing.
  - **Classification** (education/work sections, seniority, domain categories).
  - **Filling missing fields** (inferred titles/dates with confidence scores) when acceptable.
- **Risks/Costs** External dependency, per‑token cost, latency, and data privacy concerns. Keep LLM usage optional behind a feature flag and with strict budget controls.

---

## Architecture Fit (Your Stack)

- **Backend**: Flask API. Parsing, template analysis, and formatting live in `Backend/utils/*` and routes in `Backend/app.py`.
- **Frontend**: React (CRA). Communicates with Flask via `/api/...` endpoints.
- **LLM Integration Points**
  - As a **fallback** when `parse_resume` confidence is low.
  - As an **enhancer** endpoint you call on-demand for rewriting/normalizing.
  - As a **validator** to detect missing sections and suggest fixes.

Recommended approach: add a small LLM wrapper in the backend plus optional endpoints, then toggle from the UI.

---

## Models, API, and Pricing

- **OpenAI‑compatible API**. Base URL: `https://api.deepseek.com/v1` (OpenAI-compatible usage). You use the standard OpenAI SDKs by overriding `base_url` and providing your DeepSeek API key.
- **Common models**
  - `deepseek-chat` (fast, general tasks like extraction/rewriting)
  - `deepseek-reasoner` (reasoning-heavy tasks). Note: If you pass `tools` to `deepseek-reasoner`, requests are processed by `deepseek-chat` per docs.
- **Pricing**
  - Billed per token (input + output). Pricing changes; see official docs for current rates:
    - Models & Pricing: https://api-docs.deepseek.com/quick_start/pricing
    - USD details: https://api-docs.deepseek.com/quick_start/pricing-details-usd
  - Expect no permanent “free” tier. Some accounts receive promotional credits. Treat the service as paid and budget-controlled.
- **Cost estimation**
  - Cost = `tokens_in * price_in + tokens_out * price_out` (per 1M tokens rates). Estimate tokens with tiktoken-like tools or by average words≈0.75 tokens.

---

## Should You Integrate?

- **Integrate now if**
  - You handle many messy resumes, varied templates, or multilingual inputs.
  - You want better skills/section extraction with less rule maintenance.
  - You need high‑quality bullet rewriting and ATS‑friendly summaries.
- **Defer if**
  - Strict data locality/compliance prohibits sending PII to third parties.
  - SLA requires sub‑second responses for bulk processing.
  - Your current rules perform sufficiently for your use cases.

Recommendation: ship as **optional** (feature-flagged), start small with a pilot on the noisiest resumes.

---

## Backend Integration (Flask, Python)

1. **Create an API Key**
   - Sign in: https://platform.deepseek.com/
   - Create a key and copy it.

2. **Install SDK**
   - Add to your environment (do not expose in repo):
     - `pip install openai>=1.40.0`

3. **Configure environment**
   - Set `DEEPSEEK_API_KEY` in your environment or `.env` (do NOT commit secrets):
     - Windows PowerShell: `$env:DEEPSEEK_API_KEY="<your_key>"`

4. **Create a lightweight client wrapper** (e.g., `Backend/utils/llm.py`):

```python
# utils/llm.py
import os
import time
from typing import List, Dict
from openai import OpenAI

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com/v1")

DEFAULT_MODEL = "deepseek-chat"  # or "deepseek-reasoner" for complex reasoning

class LLMError(Exception):
    pass

def chat(messages: List[Dict[str, str]], model: str = DEFAULT_MODEL, timeout: int = 60,
         response_format: Dict = None, temperature: float = 0.2) -> str:
    if not DEEPSEEK_API_KEY:
        raise LLMError("DEEPSEEK_API_KEY not set")
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            timeout=timeout,
            response_format=response_format  # e.g., {"type": "json_object"}
        )
        return resp.choices[0].message.content or ""
    except Exception as e:
        raise LLMError(str(e))
```

5. **Example usage: Skills extraction with JSON output**

```python
# utils/skill_extractor.py
import json
from .llm import chat

SCHEMA_HINT = (
    "Return strict JSON with keys: skills (list[str]), tools (list[str]), summary (str)."
)

PROMPT = (
    "You are an ATS-oriented extractor. Given raw resume text, extract normalized skills "
    "and tools, plus a one-sentence professional summary."
)

def extract_skills(raw_text: str) -> dict:
    messages = [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": SCHEMA_HINT + "\n\nResume:\n" + raw_text},
    ]
    out = chat(messages, response_format={"type": "json_object"})
    return json.loads(out)
```

6. **Add an optional API route** (example pattern to follow in `Backend/app.py`):

```python
# app.py (example pattern)
from utils.skill_extractor import extract_skills

@app.route('/api/llm/skills', methods=['POST'])
def llm_skills():
    data = request.get_json(force=True)
    raw_text = data.get('text', '')
    if not raw_text:
        return jsonify({"success": False, "message": "Missing text"}), 400
    try:
        result = extract_skills(raw_text)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
```

7. **Fallback integration**
   - In `parse_resume(...)`, when confidence is low or fields are missing, call a targeted LLM helper to:
     - classify sections
     - infer missing titles/dates with confidence fields
     - rewrite bullets into STAR/impact phrasing
   - Keep original deterministic path as default and log decisions.

---

## Frontend Integration (React)

- Add a **toggle** like “Use AI Enhancement (DeepSeek)” on the upload/format page.
- When enabled, call the new backend endpoints (e.g., `/api/llm/skills`, `/api/format?use_ai=true`).
- Display disclaimers and allow users to review/accept AI edits.

Do not put API keys in the frontend. All LLM calls go through the backend.

---

## Security, Privacy, and Compliance

- Resumes contain PII. Document your data handling.
- Minimize sent content (only necessary sections). Consider redaction of phone/email if not needed for the task.
- Allow users to opt out of third‑party processing.
- Log prompts/outputs without PII when possible; protect logs.

---

## Performance and Cost Controls

- **Latency**: LLM adds 0.3–2.5s for short prompts; longer inputs take longer. Consider async jobs for batch runs.
- **Token reduction**: Pre-trim to relevant sections, summarize long text first, use concise prompts.
- **Caching**: Cache identical prompts (hash of payload) to reduce repeated costs.
- **Budgets**: Add daily/monthly caps; return graceful errors after budget exhaustion.
- **Model choice**: Prefer `deepseek-chat` for most tasks; reserve `deepseek-reasoner` for complex reasoning only.

---

## Advantages and Disadvantages

- **Advantages**
  - Better robustness on unstructured/varied resumes.
  - Higher quality extraction and rewriting.
  - Less manual rule maintenance over time.
  - Faster iteration for new formats and languages.
- **Disadvantages**
  - Ongoing per‑token cost; not “free.”
  - External dependency and vendor changes (models/pricing).
  - Data privacy/regulatory review needed for PII.
  - Nondeterminism—may require human-in-the-loop review.

---

## Alternatives

- **Local models** (no external data sharing): Llama 3.1/3.2, Qwen2.5, Mistral—inference via Ollama or vLLM. Pros: privacy and cost control; Cons: infra + quality tuning.
- **Other APIs**: OpenAI, Anthropic, Azure OpenAI. Consider cost/quality/compliance trade-offs.
- **Non-LLM**: Improve current heuristics/regex, expand rule coverage, and add doc layout features.

---

## Rollout Plan

1. Add backend wrapper and one endpoint (skills extraction) behind a feature flag.
2. Instrument metrics: token counts, latency, failure rate, edit acceptance rate.
3. Run A/B on messy resumes; compare extraction accuracy and user acceptance.
4. If positive, expand to rewriting and section classification.
5. Add budgets and monitoring dashboards.

---

## FAQ

- **Is DeepSeek free?** No. It’s billed per token. Some accounts may get limited promotional credits; always plan for paid usage.
- **Where do I see current prices?** Official page: https://api-docs.deepseek.com/quick_start/pricing and USD details page.
- **Which model should I start with?** `deepseek-chat` for general extraction/rewriting; use `deepseek-reasoner` only if you truly need deeper reasoning.
- **Will this slow my pipeline?** Yes, modestly. Keep LLM optional and use async for batch.

---

## Appendix: Minimal Python Call Examples

```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com/v1")

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "Rewrite for ATS clarity."},
        {"role": "user", "content": "Bullet: Improved system performance by 30% by optimizing SQL queries."},
    ],
    temperature=0.2,
)
print(resp.choices[0].message.content)
```

For JSON‑only responses (if supported), pass `response_format={"type": "json_object"}` and `json.loads(...)` the result.
