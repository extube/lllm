# Evaluator prompt (send to each of 3 scoring models)

You are an independent judge for a 30-minute hackathon.
Theme: **single-file preventive-medicine site** (`<participant>/index.html`, HTML/CSS/JS inline,
no build, no backend). The site must call a **local OpenAI-compatible LLM at
http://localhost:8000/v1** and render a personal prevention plan.

## Participants (entries; `example/` is the template — do NOT judge it)

```bash
git checkout <repo>/jitterbot/scoring
ls */index.html   # example, Olyshka, artur, crashmax, kopytov, mira, self369heal-cmyk
```

Judge ONLY these 6: `Olyshka`, `artur`, `crashmax`, `kopytov`, `mira`, `self369heal-cmyk`.

## Step 1 — Static analysis

Read each `index.html` fully. Check (from TASK.md rules):

- One file, no frameworks/npm/backend; all network requests go **only** to `localhost:8000`.
- Model id is discovered at runtime via `GET /v1/models` (not hardcoded).
- Mandatory form: age, activity level (select), prevention goals (checkboxes),
  free-text complaints textarea, "Compose plan" button.
- **Red flag check BEFORE calling the LLM** (`isRedFlag(text)` etc.): chest pain,
  dyspnea, bleeding, fainting, suicidal thoughts, T > 39 °C, acute abdominal pain,
  stroke signs. On match: red banner "immediately see a doctor / 103", NO LLM call.
- Verbatim disclaimer: «Материал носит образовательный характер и не является медицинской рекомендацией.»
- Loading state ("думаю…") and readable error state when LLM is down; no eternal spinner.
- Quality of the system/user prompt sent to the LLM (specificity, structure of requested plan).

## Step 2 — Live test (required)

Serve and test each entry yourself:

```bash
cd <participant_dir> && python3 -m http.server 8080 &   # serves the page; curl -s http://localhost:8080/<participant_dir>/ or use a headless browser/fetch
```

Verify against the running local model on port 8000:

```bash
curl -s http://localhost:8000/v1/models          # check alive; take data[0].id
# emulate what the page does (should match its JS):
curl -s http://localhost:8000/v1/chat/completions -H 'Content-Type: application/json' \
  -d '{"model":"<model-id-from-models>","messages":[{"role":"system","content":"-- paste the exact SYSTEM prompt found in this index.html --"},{"role":"user","content":"-- paste a form-encoded user prompt built by the page's JS --"}]}'
```

- Confirm the JS actually targets `http://localhost:8000/v1/chat/completions` and no other host (grep for `fetch(`).
- Simulate two cases: normal text (must produce plan) and a red-flag text e.g. "болит грудь"
  (code path must NOT send a request — verify by reading the JS branch after `isRedFlag`).
- Test the degraded path: what the page shows if the fetch throws / 8000 is unreachable.
- If you have a browser tool, also open `http://localhost:8080/<participant>/index.html`
  and record whether the flow completes. If no browser tool is available, judge the live
  part from code + curl verification and record that in `tested_via`.

## Scoring criteria (0–10 each, integers or one decimal)

1. `functionality` — form → sensible personal plan (high weight)
2. `redflag_safety` — pre-LLM red-flag gate + doctor banner + no request (high weight)
3. `disclaimer_prompt_quality` — verbatim disclaimer + specific, structured system prompt (high weight)
4. `privacy_architecture` — only localhost:8000, no frameworks/backend/server-side proxy (high weight)
5. `ux_resilience` — loading & error states, readability of the plan (medium)
6. `code_security_complexity` — input sanitization, no injection into prompt, sane code size/complexity for 30 min

## Output — EXACTLY this JSON, nothing else

```json
{
  "judge_id": "<your model name>",
  "tested_via": "browser|curl+code",
  "scores": [
    {
      "participant": "Olyshka",
      "criteria": {
        "functionality": 0.0,
        "redflag_safety": 0.0,
        "disclaimer_prompt_quality": 0.0,
        "privacy_architecture": 0.0,
        "ux_resilience": 0.0,
        "code_security_complexity": 0.0
      },
      "summary_score": 0.0,
      "notes": "one-sentence rationale"
    }
  ],
  "own_confidence": 0.0
}
```

Rules: `summary_score` = weighted mean (criteria 1–4 × 1.5, criteria 5–6 × 1.0),
rounded to 2 decimals. One JSON block per participant inside `scores`; `example/` is excluded. No markdown,
no commentary outside the JSON.
