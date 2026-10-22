# Olyshka

Mean summary: 9.03

## opencode-go/glm-5.3-flash
```json
{
 "participant": "Olyshka",
 "criteria": {
  "functionality": 8.5,
  "redflag_safety": 9.0,
  "disclaimer_prompt_quality": 9.5,
  "privacy_architecture": 10.0,
  "ux_resilience": 9.0,
  "code_security_complexity": 9.0
 },
 "summary_score": 9.19,
 "notes": "Live call produced a well-structured sectioned plan; red-flag gate (ё-normalized, Cyrillic-aware, catches «болит грудь» and «болит живот» in executed-node test) fires pre-LLM with spec banner; verbatim disclaimer on page, in plan and forced into LLM output format; only-localhost fetches, safe textContent rendering, elapsed-timer loading and clean error state."
}
```

- redflag_safety: 9.0
- privacy_architecture: 10.0
- disclaimer_prompt_quality: 9.5
- functionality: 8.5
- ux_resilience: 9.0
- code_security_complexity: 9.0
- notes: Live call produced a well-structured sectioned plan; red-flag gate (ё-normalized, Cyrillic-aware, catches «болит грудь» and «болит живот» in executed-node test) fires pre-LLM with spec banner; verbatim disclaimer on page, in plan and forced into LLM output format; only-localhost fetches, safe textContent rendering, elapsed-timer loading and clean error state.
## opencode-go/mimo-v2.6-flash
```json
{
 "participant": "Olyshka",
 "criteria": {
  "functionality": 9.0,
  "redflag_safety": 9.5,
  "disclaimer_prompt_quality": 9.5,
  "privacy_architecture": 9.5,
  "ux_resilience": 9.0,
  "code_security_complexity": 8.5
 },
 "summary_score": 9.22,
 "notes": "Full form->live plan verified via curl (18.6s, structured sections + disclaimer), red-flag battery 9/9 including the required 'болит грудь' blocks the request before any fetch, verbatim disclaimer shown 3 times, only localhost:8000, elapsed-second loader and clear error state; minor: live plan missed the 'Сон' section, status line uses innerHTML with err.message and no prompt-injection guard."
}
```

- redflag_safety: 9.5
- privacy_architecture: 9.5
- disclaimer_prompt_quality: 9.5
- functionality: 9.0
- ux_resilience: 9.0
- code_security_complexity: 8.5
- notes: Full form->live plan verified via curl (18.6s, structured sections + disclaimer), red-flag battery 9/9 including the required 'болит грудь' blocks the request before any fetch, verbatim disclaimer shown 3 times, only localhost:8000, elapsed-second loader and clear error state; minor: live plan missed the 'Сон' section, status line uses innerHTML with err.message and no prompt-injection guard.
## qwen3.7-plus
```json
{
 "participant": "Olyshka",
 "criteria": {
  "functionality": 8.0,
  "redflag_safety": 9.0,
  "disclaimer_prompt_quality": 9.0,
  "privacy_architecture": 9.0,
  "ux_resilience": 9.0,
  "code_security_complexity": 8.0
 },
 "summary_score": 8.69,
 "notes": "Well-structured 4-section system prompt that itself requires the model to emit the verbatim disclaimer, 9 Cyrillic-aware red-flag regexes, createElement-based rendering with spinner/timer, and a clear 103/112 banner; minor ding because one h3 uses innerHTML (though with hardcoded icon, not user data)."
}
```

- redflag_safety: 9.0
- privacy_architecture: 9.0
- disclaimer_prompt_quality: 9.0
- functionality: 8.0
- ux_resilience: 9.0
- code_security_complexity: 8.0
- notes: Well-structured 4-section system prompt that itself requires the model to emit the verbatim disclaimer, 9 Cyrillic-aware red-flag regexes, createElement-based rendering with spinner/timer, and a clear 103/112 banner; minor ding because one h3 uses innerHTML (though with hardcoded icon, not user data).
