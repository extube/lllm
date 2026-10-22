# Hackathon scoring — how to run

## Prerequisites
- opencode CLI installed (`/root/.opencode/bin/opencode`), authenticated with your GO subscription.
- Local LLM live on `:8000` (`curl http://localhost:8000/v1/models`) — the judged sites use it.
- Repo on branch `jitterbot/scoring`.

## One command for the whole pipeline

```bash
sh judge/run.sh
# swap models: J1=opencode/glm-4.6-flash J2=... J3=... FINAL=opencode/glm-5.3 sh judge/run.sh
```

## What it does, step by step

1. **Round 1 — evaluation (parallelizable if you want speed, script runs sequentially).**
   The SAME prompt (`judge/evaluator-prompt.md`) goes to three cloud judges via
   `opencode run --model <id>`. Each judge:
   - statically reads all six `index.html` files,
   - starts `python3 -m http.server 8080` per entry and curl-tests the page's
     system/user prompt against `localhost:8000/v1/chat/completions`,
   - verifies red-flag path blocks the request, error states, privacy,
   - returns the fixed JSON schema (6 participants × 6 criteria, weights in prompt).
2. **`judge/pipeline.py`**: parses each judge output (first JSON object extracted from the
   log), computes mean `summary_score` per participant, disqualifies hard-requirement
   failures, and sends all three reports + rubric to the **final model** (chair judge) →
   `{"winner","ranking","reason"}`.
3. **Voting.** Same three judge models get the verdict and answer
   `{"judge_id","agree":true|false}`. **If ≥2 disagree → the three judges rerun scoring
   (fresh round, logs `*-r2`)** and the final model issues a new, binding verdict.
4. **Artifacts** land in `judge/results/`:

| File | Content |
|---|---|
| `log-judge{1,2,3}.txt` | raw agent transcript (incl. commands it ran) = decision log |
| `judge{1,2,3}.json` | the extracted report per judge |
| `log-final-r1.txt` | final model's reasoning + verdict |
| `votes-r1.json` | per-judge agree/disagree votes |
| `winner.json` | winner + tiers + reason |
| `tierlist.md` | S/A/B/C tier table (mean score, hard-req fails) |
| `analytics-<participant>.md` | per-project: every judge's criteria scores + notes |
| `log-final-r2.txt`, `*-r2` | second round (only if triggered) |

## Model assignment (cloud, GO subscription)

| Role | Default (in scripts) |
|---|---|
| Judge 1 | `opencode/GLM-5.3-Flash` |
| Judge 2 | `opencode/MiMo-V2.6-Flash` |
| Judge 3 | `opencode/Qwen3.7-Plus` |
| Final | `opencode/MiniMax-M3` |

Adjust ids to whatever your plan exposes (`opencode models` lists them).

## Human check before trusting the result
- Skim `log-judge*.txt`: did each judge actually run the curl tests (not just static read)?
- Check `votes-r1.json` — a rerun that produced identical disagreement = strong signal to
  judge manually.
- `tierlist.md` is a suggestion; final call is yours.
