# Final-vote logic

## Final verdict prompt (send to final LLM)

You are the chair judge. You receive three judging reports in this exact JSON schema:

```json
{"judge_id":"...","tested_via":"browser|curl+code","scores":[{"participant":"...","criteria":{"functionality":0.0,"redflag_safety":0.0,"disclaimer_prompt_quality":0.0,"privacy_architecture":0.0,"ux_resilience":0.0,"code_security_complexity":0.0},"summary_score":0.0,"notes":"..."}]}
```

Compute the mean `summary_score` per participant across the three judges, break ties in
favor of higher `redflag_safety` and `privacy_architecture` (they are hard requirements).
Flag any participant that failed a hard requirement (red-flag gate missing, disclaimer
missing, or requests to a non-local host) as disqualified from winning.

Return EXACTLY:

```json
{"winner":"<participant>","ranking":[{"participant":"...","mean_score":0.0,"hard_requirement_fail":false}],"reason":"2-3 sentences","used_tiebreak":false}
```

## Voting / disagreement rule

Send the final verdict JSON back to the 3 evaluator models with:
"A further judge chose X as the winner. Answer ONLY
`{"judge_id":"...","agree":true}` or `{"judge_id":"...","agree":false,"preferred":"..."}`."
If ≥2 judges disagree → rerun the full scoring round (fresh evaluator prompts) once, then
take the new final verdict; the second verdict is final.
