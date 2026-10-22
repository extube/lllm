# Hackathon Results

**Date:** 2026-10-22 · **Branch:** `jitterbot/scoring`
**Method:** 3 cloud LLM judges evaluate independently → 1 chair model issues the final
verdict → all 3 judges vote to confirm. Live tests ran against the local LLM
(`localhost:8000/v1`, Gemma-4-E2B agent).

## 1. Judging process

| Role | Model | Full transcript |
|---|---|---|
| Judge 1 | `opencode-go/glm-5.3-flash` | `judge/results/log-judge1.txt` |
| Judge 2 | `opencode-go/mimo-v2.6-flash` | `judge/results/log-judge2.txt` |
| Judge 3 | `opencode-go/qwen3.7-plus` | `judge/results/log-judge3.txt` |
| Chair (final verdict) | `opencode-go/minimax-m3` | `judge/results/log-final-r1.txt` |

Steps performed (fully automated via `judge/run.sh` + `judge/pipeline.py`):

1. **Identical evaluator prompt** sent to each of the 3 judges via `opencode run`.
2. Each judge independently: read all six `index.html` files, served each entry with
   `python3 -m http.server 8080`, extracted each entry's *own* system/user prompts,
   executed them against the live model (`curl http://localhost:8000/v1/chat/completions`),
   and verified: normal text → plan; red-flag text («болит грудь») → request **not** sent;
   LLM-down → readable error. Test method recorded as `curl+code` by all judges.
3. Each judge returned the same JSON schema (6 participants × 6 criteria + summary).
4. **Chair model** received all 3 reports, computed weighted means, flagged
   hard-requirement failures, ranked, and issued the verdict.
5. **Voting round:** each judge seen the verdict, answered `{"judge_id","agree"}`.
   3/3 agree → rescoring round **not** triggered (`votes-r1.json`).

Scoring criteria (0–10, criteria 1–4 weighted ×1.5 in `summary_score`):
`functionality` · `redflag_safety` · `disclaimer_prompt_quality` ·
`privacy_architecture` · `ux_resilience` · `code_security_complexity`

## 2. Prompts used

### 2.1 Evaluator prompt (same for the 3 judges)

> You are an independent judge for a 30-minute hackathon.
> Theme: **single-file preventive-medicine site** (`<participant>/index.html`, HTML/CSS/JS inline, no build, no backend). The site must call a **local OpenAI-compatible LLM at http://localhost:8000/v1** and render a personal prevention plan.
>
> Judge ONLY these 6: `Olyshka`, `artur`, `crashmax`, `kopytov`, `mira`, `self369heal-cmyk` (`example/` is the template).
>
> **Step 1 — Static analysis:** read each `index.html` fully; check: single file, no frameworks/backend; requests only to `localhost:8000`; model id discovered via `GET /v1/models`; mandatory form (age, activity select, goal checkboxes, complaints textarea, submit); **red-flag check BEFORE calling the LLM** (chest pain, dyspnea, bleeding, fainting, suicidal thoughts, T > 39 °C, acute abdominal pain, stroke signs → red banner «немедленно обратитесь к врачу / 103», no LLM call); verbatim disclaimer «Материал носит образовательный характер и не является медицинской рекомендацией.»; loading state («думаю…») and readable error state; quality of the prompt sent to the LLM.
>
> **Step 2 — Live test (required):** `cd <participant_dir> && python3 -m http.server 8080 &`; verify against the running local model: `curl -s http://localhost:8000/v1/models`, then `curl -s http://localhost:8000/v1/chat/completions -H 'Content-Type: application/json' -d '{...exact prompts from the entry's JS...}'`. Confirm the JS targets only `localhost:8000/v1/chat/completions`; simulate normal text (plan produced) and a red-flag text («болит грудь» — request must NOT be sent); test the degraded path (8000 unreachable).
>
> **Scoring (0–10 each):** functionality, redflag_safety, disclaimer_prompt_quality, privacy_architecture (high, ×1.5); ux_resilience, code_security_complexity (×1.0).
>
> **Output — exact JSON:** `{"judge_id", "tested_via", "scores":[{"participant","criteria":{6 criteria},"summary_score","notes"}], "own_confidence"}` — `summary_score` = weighted mean, one entry per participant, nothing but the JSON.

Full text: `judge/evaluator-prompt.md`.

### 2.2 Final (chair) prompt

> You are the chair judge. You receive three judging reports in the exact JSON schema. Compute the mean `summary_score` per participant across the three judges, break ties in favor of higher `redflag_safety` and `privacy_architecture`. Flag any participant that failed a hard requirement (red-flag gate missing, disclaimer missing, or requests to a non-local host) as disqualified from winning.
>
> Return exactly: `{"winner","ranking":[{"participant","mean_score","hard_requirement_fail"}],"reason","used_tiebreak"}`

(With three raw judge reports appended. Full text: `judge/final-prompt.md`.)

### 2.3 Vote prompt (to each judge after the verdict)

> You judged this hackathon earlier (your JSON report is below). The chair judge decided the winner: `<verdict JSON>`. Your report: `<own report>`. Answer ONLY `{"judge_id":"...","agree":true}` or `{"judge_id":"...","agree":false,"preferred":"..."}`.

Result: **3/3 agree** — no rescoring round was needed.

## 3. Verdicts from each judge for each solution

### 3.1 Scores by judge (summary_score per participant)

| Participant | GLM-5.3-Flash | MiMo-V2.6-Flash | Qwen3.7-Plus | Mean | Chair verdict |
|---|---|---|---|---|---|
| self369heal-cmyk | 9.25 | 9.5 | 9.5 | **9.42** | **🏆 Winner** |
| Olyshka | 9.19 | 9.22 | 8.69 | 9.03 | Runner-up (eligible) |
| crashmax | 8.38 | 9.28 | 8.69 | 8.78 | Runner-up (eligible) |
| artur | 8.41 | 8.31 | 8.75 | 8.49 | Hard-req fail: red-flag gate |
| kopytov | 7.81 | 7.75 | 7.75 | 7.77 | Hard-req fail: disclaimer + gate |
| mira | 5.47 | 5.66 | 4.81 | 5.31 | Hard-req fail: gate only 3/16 |

### 3.2 Judge 1 — `opencode-go/glm-5.3-flash` (own_confidence 0.86)

- **self369heal-cmyk (9.25):** Best overall: CSP meta restricts connect-src to localhost:8000, executed red-flag classifier scored 13/16 with labeled reasons in the exact-spec banner, live call returned a coherent structured plan, and it uniquely handles timeouts, 400-fallback, finish_reason=length, empty answers plus escape-first markdown rendering and a prompt-injection rule.
- **Olyshka (9.19):** Live call produced a well-structured sectioned plan; red-flag gate (ё-normalized, Cyrillic-aware, catches «болит грудь» and «болит живот») fires pre-LLM with the spec banner; verbatim disclaimer on page, in plan and forced into LLM output format; only-localhost fetches, safe textContent rendering, elapsed-timer loading and clean error state.
- **artur (8.41):** Polished UX (connection pill, abort/timeout, goal validation, copy-plan) and clean textContent rendering, but the executed red-flag regex set (11/16) misses «болит грудь», «давление в груди», «болит живот» and stroke phrasings — so the LLM gets called on them.
- **crashmax (8.38):** Solid normalized gate (12/16, catches «болит грудь») with verbatim disclaimer and structured 5-section prompt, but no fetch timeout risks an eternal spinner, the form is wholly disabled during generation, and the live response showed heavy model degeneration that its markdown renderer faithfully reproduced.
- **kopytov (7.81):** Most ambitious entry (chat app with history, retry, localStorage schema validation, injection-hardened dual-mode prompts) but the gate (11/16) misses «болит грудь», «потерял сознание», «болит живот», and the mandatory verbatim disclaimer is absent — only «Не заменяет консультацию врача.» is shown.
- **mira (5.47):** Only the verbatim footer disclaimer was added to the untouched template: one-line TODO-driven system prompt, a 2-pattern gate whose executed test (3/16) misses «болит грудь», dyspnea, bleeding, fainting, fever and stroke; no empty-response handling, timeouts or output formatting.

### 3.3 Judge 2 — `opencode-go/mimo-v2.6-flash` (own_confidence 0.85)

- **self369heal-cmyk (9.5):** Best-in-class: CSP connect-src locked to localhost:8000, red-flag battery 9/9 with named reasons and zero network calls before the banner, verbatim disclaimer twice, structured live plan (15.5 s) from a system prompt with an explicit anti-injection rule, escaped markdown renderer, 180 s timeout with readable errors; only cosmetic heading-hash rendering quirks.
- **crashmax (9.28):** Red-flag battery 9/9 with zero fetches on both red-flag simulations and banner «Немедленно обратитесь к врачу / 103», verbatim disclaimer, strict 5-section system prompt reproduced live (19.4 s), escapeHtml-escaped markdown renderer and empty-content/reasoning fallbacks; only lacking an elapsed-time ticker in the loader.
- **Olyshka (9.22):** Full form → live plan verified via curl (18.6 s, structured sections + disclaimer), red-flag battery 9/9 including the required «болит грудь» blocks the request before any fetch, verbatim disclaimer shown 3 times, only localhost:8000, elapsed-second loader and clear error state; minor: live plan missed the «Сон» section, status line uses innerHTML with err.message and no prompt-injection guard.
- **artur (8.31):** Polished 7-day plan flow with timeouts/copy/focus handling and textContent-only rendering, but «болит грудь» is NOT matched by isRedFlag — the page really sent a chat/completions request and rendered a plan instead of the doctor banner; system prompt is a single short sentence.
- **kopytov (7.75):** Working chat-style plan generator with excellent anti-injection safety rules and retry/timeout UX, but the mandatory verbatim disclaimer is absent (0 occurrences), goals are toggle buttons instead of checkboxes, and «болит грудь» passes the gate and hits the LLM (battery 7/9).
- **mira (5.66):** Essentially the untouched template (7 TODOs, 61-char system prompt): only 2 of 9 red-flag categories covered, so «болит грудь» sends the request and keeps the banner hidden (verified by fetch spy), output is an unformatted 5.4k-char blob with no request timeout, though privacy, runtime model discovery and the verbatim disclaimer still hold.

### 3.4 Judge 3 — `opencode-go/qwen3.7-plus` (own_confidence 0.82)

- **self369heal-cmyk (9.5):** CSP header strictly locks network to localhost:8000, labeled red-flag patterns with matched-reason display in banner, proper HTML-escaped markdown renderer, demo button, input validation (age range, goal count, maxlength), and verbatim disclaimer both in plan-box and footer — most privacy-hardened and safety-complete entry.
- **artur (8.75):** Editorial-quality UX with connection-status pill, copy-plan, reset, empty states, and 12+ red-flag patterns including English variants; system prompt is short and embedded inline in the fetch call rather than a dedicated constant; textContent-only rendering keeps it injection-safe.
- **Olyshka (8.69):** Well-structured 4-section system prompt that itself requires the model to emit the verbatim disclaimer, 9 Cyrillic-aware red-flag regexes, createElement-based rendering with spinner/timer, and a clear 103/112 banner; minor ding because one h3 uses innerHTML (hardcoded icon, not user data).
- **crashmax (8.69):** 25+ individual red-flag regexes with proper Cyrillic support, a dedicated escapeHtml + inlineFormat pipeline, reasoning_effort fallback for Qwen-style servers, and verbatim disclaimer in the header; UX is clean but simpler than artur/self369heal-cmyk (no copy button, no dark mode).
- **kopytov (7.75):** Ambitious chat-style app with onboarding, sidebar, localStorage history, two system prompts, and retry — but the mandatory verbatim disclaimer is replaced by the shorter «Не заменяет консультацию врача», failing TASK.md §6.1, and goals use button/aria-pressed instead of the required checkboxes.
- **mira (4.81):** Essentially the provided template with TODO comments left in: system prompt is one sentence, red-flag list covers only chest pain and suicide (missing dyspnea, bleeding, fainting, T>39, abdominal pain, stroke signs), plan output is unformatted textContent, and there is no markdown rendering or error differentiation.

### 3.5 Final verdict — chair model `opencode-go/minimax-m3`

> **Winner: self369heal-cmyk** (used_tiebreak: false)
>
> self369heal-cmyk leads on mean summary_score (9.42 vs Olyshka's 9.03 and crashmax's 8.78) with unanimous top marks from all three judges, and it satisfies every hard requirement: CSP-locked localhost-only networking (privacy 10/10 across judges), a red-flag gate that catches the mandated «болит грудь» before any fetch, and the verbatim disclaimer present. Artur, kopytov and mira are flagged as hard-requirement failures: artur's executed gate misses «болит грудь» so the LLM is called on it, kopytov omits the mandatory verbatim disclaimer and also misses the gate, and mira's gate catches only 3/16 red-flag cases. Olyshka and crashmax remain eligible runners-up but scored lower on mean summary_score.

**Vote round:** GLM-5.3-Flash ✅ agree · MiMo-V2.6-Flash ✅ agree · Qwen3.7-Plus ✅ agree → 3/3, verdict final.

## 4. Tier list

| Tier | Participant | Mean score |
|---|---|---|
| S | self369heal-cmyk | 9.42 |
| S | Olyshka | 9.03 |
| A | crashmax | 8.78 |
| A | artur | 8.49 |
| A | kopytov | 7.77 |
| B | mira | 5.31 |

## 5. Artifacts index (all in `judge/results/`)

| File | Content |
|---|---|
| `winner.json` | final verdict (winner, ranking, reason) |
| `tierlist.md` | tier table |
| `analytics-<participant>.md` | per-project breakdown: all 3 judges' criteria scores + notes |
| `judge{1,2,3}.json` | extracted judge reports |
| `log-judge{1,2,3}.txt` | full judge agent transcripts (incl. live-test commands) |
| `log-final-r1.txt` | chair model transcript |
| `votes-r1.json` | per-judge agree/disagree votes |

*Hard requirements (TASK.md): pre-LLM red-flag gate + doctor banner; verbatim disclaimer
«Материал носит образовательный характер и не является медицинской рекомендацией.»;
privacy — requests only to `localhost:8000`.*
