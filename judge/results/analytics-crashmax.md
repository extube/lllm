# crashmax

Mean summary: 8.78

## opencode-go/glm-5.3-flash
```json
{
 "participant": "crashmax",
 "criteria": {
  "functionality": 7.5,
  "redflag_safety": 8.0,
  "redflag-normalized": null,
  "disclaimer_prompt_quality": 8.5,
  "privacy_architecture": 10.0,
  "ux_resilience": 7.5,
  "code_security_complexity": 8.5
 },
 "summary_score": 8.38,
 "notes": "Solid normalized gate (12/16, catches «болит грудь») with verbatim disclaimer and structured 5-section prompt, but no fetch timeout risks an eternal spinner if the server stalls, the form is wholly disabled during generation, and the live response showed heavy model degeneration that its markdown renderer faithfully reproduced."
}
```

- redflag_safety: 8.0
- privacy_architecture: 10.0
- disclaimer_prompt_quality: 8.5
- functionality: 7.5
- ux_resilience: 7.5
- code_security_complexity: 8.5
- notes: Solid normalized gate (12/16, catches «болит грудь») with verbatim disclaimer and structured 5-section prompt, but no fetch timeout risks an eternal spinner if the server stalls, the form is wholly disabled during generation, and the live response showed heavy model degeneration that its markdown renderer faithfully reproduced.
## opencode-go/mimo-v2.6-flash
```json
{
 "participant": "crashmax",
 "criteria": {
  "functionality": 9.0,
  "redflag_safety": 9.5,
  "disclaimer_prompt_quality": 9.5,
  "privacy_architecture": 9.5,
  "ux_resilience": 9.0,
  "code_security_complexity": 9.0
 },
 "summary_score": 9.28,
 "notes": "Red-flag battery 9/9 with zero fetches on both red-flag simulations and banner 'Немедленно обратитесь к врачу / 103', verbatim disclaimer, strict 5-section system prompt reproduced live (19.4s), escapeHtml-escaped markdown renderer and empty-content/reasoning fallbacks; only lacking an elapsed-time ticker in the loader."
}
```

- redflag_safety: 9.5
- privacy_architecture: 9.5
- disclaimer_prompt_quality: 9.5
- functionality: 9.0
- ux_resilience: 9.0
- code_security_complexity: 9.0
- notes: Red-flag battery 9/9 with zero fetches on both red-flag simulations and banner 'Немедленно обратитесь к врачу / 103', verbatim disclaimer, strict 5-section system prompt reproduced live (19.4s), escapeHtml-escaped markdown renderer and empty-content/reasoning fallbacks; only lacking an elapsed-time ticker in the loader.
## qwen3.7-plus
```json
{
 "participant": "crashmax",
 "criteria": {
  "functionality": 8.0,
  "redflag_safety": 9.0,
  "disclaimer_prompt_quality": 9.0,
  "privacy_architecture": 9.0,
  "ux_resilience": 8.0,
  "code_security_complexity": 9.0
 },
 "summary_score": 8.69,
 "notes": "25+ individual red-flag regexes with proper Cyrillic support, a dedicated escapeHtml + inlineFormat pipeline, reasoning_effort fallback for Qwen-style servers, and verbatim disclaimer in the header; UX is clean but simpler than artur/self369heal-cmyk (no copy button, no dark mode)."
}
```

- redflag_safety: 9.0
- privacy_architecture: 9.0
- disclaimer_prompt_quality: 9.0
- functionality: 8.0
- ux_resilience: 8.0
- code_security_complexity: 9.0
- notes: 25+ individual red-flag regexes with proper Cyrillic support, a dedicated escapeHtml + inlineFormat pipeline, reasoning_effort fallback for Qwen-style servers, and verbatim disclaimer in the header; UX is clean but simpler than artur/self369heal-cmyk (no copy button, no dark mode).
