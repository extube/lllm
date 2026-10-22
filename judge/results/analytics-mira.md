# mira

Mean summary: 5.31

## opencode-go/glm-5.3-flash
```json
{
 "participant": "mira",
 "criteria": {
  "functionality": 5.5,
  "redflag_safety": 3.0,
  "disclaimer_prompt_quality": 4.0,
  "privacy_architecture": 10.0,
  "ux_resilience": 5.0,
  "code_security_complexity": 5.0
 },
 "summary_score": 5.47,
 "notes": "Only the verbatim footer disclaimer was added to the untouched template: one-line TODO-driven system prompt, a 2-pattern gate whose executed test (3/16) misses «болит грудь», dyspnea, bleeding, fainting, fever and stroke, plus no empty-response handling, timeouts or output formatting."
}
```

- redflag_safety: 3.0
- privacy_architecture: 10.0
- disclaimer_prompt_quality: 4.0
- functionality: 5.5
- ux_resilience: 5.0
- code_security_complexity: 5.0
- notes: Only the verbatim footer disclaimer was added to the untouched template: one-line TODO-driven system prompt, a 2-pattern gate whose executed test (3/16) misses «болит грудь», dyspnea, bleeding, fainting, fever and stroke, plus no empty-response handling, timeouts or output formatting.
## opencode-go/mimo-v2.6-flash
```json
{
 "participant": "mira",
 "criteria": {
  "functionality": 6.5,
  "redflag_safety": 3.0,
  "disclaimer_prompt_quality": 3.5,
  "privacy_architecture": 9.5,
  "ux_resilience": 5.5,
  "code_security_complexity": 6.0
 },
 "summary_score": 5.66,
 "notes": "Essentially the untouched template (7 TODOs, 61-char system prompt): only 2 of 9 red-flag categories covered, so 'болит грудь' sends the request and keeps the banner hidden (verified by fetch spy), output is an unformatted 5.4k-char blob with no request timeout, though privacy, runtime model discovery and the verbatim disclaimer still hold."
}
```

- redflag_safety: 3.0
- privacy_architecture: 9.5
- disclaimer_prompt_quality: 3.5
- functionality: 6.5
- ux_resilience: 5.5
- code_security_complexity: 6.0
- notes: Essentially the untouched template (7 TODOs, 61-char system prompt): only 2 of 9 red-flag categories covered, so 'болит грудь' sends the request and keeps the banner hidden (verified by fetch spy), output is an unformatted 5.4k-char blob with no request timeout, though privacy, runtime model discovery and the verbatim disclaimer still hold.
## qwen3.7-plus
```json
{
 "participant": "mira",
 "criteria": {
  "functionality": 4.0,
  "redflag_safety": 2.0,
  "disclaimer_prompt_quality": 4.0,
  "privacy_architecture": 9.0,
  "ux_resilience": 4.0,
  "code_security_complexity": 6.0
 },
 "summary_score": 4.81,
 "notes": "Essentially the provided template with TODO comments left in: system prompt is one sentence, red-flag list covers only chest pain and suicide (missing dyspnea, bleeding, fainting, T>39, abdominal pain, stroke signs), plan output is unformatted textContent, and there is no markdown rendering or error differentiation."
}
```

- redflag_safety: 2.0
- privacy_architecture: 9.0
- disclaimer_prompt_quality: 4.0
- functionality: 4.0
- ux_resilience: 4.0
- code_security_complexity: 6.0
- notes: Essentially the provided template with TODO comments left in: system prompt is one sentence, red-flag list covers only chest pain and suicide (missing dyspnea, bleeding, fainting, T>39, abdominal pain, stroke signs), plan output is unformatted textContent, and there is no markdown rendering or error differentiation.
