"""Aggregate judge reports -> final verdict -> vote -> (rerun once) -> artifacts."""
import json, os, re, subprocess, sys

PARTS = ["Olyshka", "artur", "crashmax", "kopytov", "mira", "self369heal-cmyk"]
HARD = {"redflag_safety", "disclaimer_prompt_quality", "privacy_architecture"}
CRIT = list(HARD) + ["functionality", "ux_resilience", "code_security_complexity"]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.abspath(sys.argv[1])
os.chdir(ROOT)
FINAL = sys.argv[2]
J1 = os.environ.get("J1", "opencode-go/glm-5.3-flash")
J2 = os.environ.get("J2", "opencode-go/mimo-v2.6-flash")
J3 = os.environ.get("J3", "opencode-go/qwen3.7-plus")


def rerun_judges():
    # disagreement -> fresh scoring round with the same evaluator prompt
    prompt = open("judge/evaluator-prompt.md").read()
    for i, m in ((1, J1), (2, J2), (3, J3)):
        r = subprocess.run(["opencode", "run", "--model", m, "--", prompt],
                           capture_output=True, text=True, cwd=RES)
        raw = os.path.join(RES, f"log-judge{i}-r2.txt")
        open(raw, "w").write(r.stdout + "\n-- STDERR --\n" + r.stderr)
        mm = re.search(r"\{.*\}", r.stdout, re.S)
        if mm:
            json.dump(json.loads(mm.group(0)),
                      open(os.path.join(RES, f"judge{i}.json"), "w"), ensure_ascii=False, indent=2)


def oc(model, prompt, log):
    print(f"== {log} with {model}")
    r = subprocess.run(["opencode", "run", "--model", model, "--", prompt],
                       capture_output=True, text=True, cwd=ROOT)
    open(os.path.join(RES, log), "w").write(r.stdout + "\n-- STDERR --\n" + r.stderr)
    m = re.search(r"\{.*\}", r.stdout, re.S)
    return json.loads(m.group(0)) if m else {}


def scores_of(reports):
    per = {}
    for rep in reports:
        for s in rep.get("scores", []):
            per.setdefault(s["participant"], []).append((rep.get("judge_id", "?"), s))
    return per


def mean(reports, p):
    ss = [s["summary_score"] for _, s in scores_of(reports).get(p, [])]
    return round(sum(ss) / len(ss), 2) if ss else None


def final_round(reports, tag):
    block = json.dumps(reports, ensure_ascii=False, indent=1)
    prompt = (open("judge/final-prompt.md").read().split("## Voting")[0]
              + "\n\n## Reports\n" + block)
    verdict = oc(FINAL, prompt, f"log-final-{tag}.txt")
    agree = 0
    votes = []
    ev_prompt = ("You judged this hackathon earlier (your JSON report is below).\n"
                 "The chair judge decided the winner: " + json.dumps(verdict)
                 + "\n\nYour report:\n" + json.dumps(reports, ensure_ascii=False)
                 + "\nAnswer ONLY {\"judge_id\":\"...\",\"agree\":true} or "
                 + "{\"judge_id\":\"...\",\"agree\":false,\"preferred\":\"...\"}.")
    for i, j in enumerate([(J1, "vote1"), (J2, "vote2"), (J3, "vote3")]):
        v = oc(j[0], ev_prompt, j[1] + f"-{tag}.txt")
        votes.append(v)
        if v.get("agree", True):
            agree += 1
    open(os.path.join(RES, f"votes-{tag}.json"), "w").write(json.dumps(votes, indent=2))
    return verdict, agree


def artifacts(reports, verdict):
    per = scores_of(reports)
    tier = sorted(PARTS, key=lambda p: mean(reports, p) or 0, reverse=True)
    ranks = []
    for i, p in enumerate(tier):
        entry = {"tier": "S" if i < len(tier) * .2 and mean(reports, p) > 7
                      else "A" if mean(reports, p) >= 6
                      else "B" if mean(reports, p) >= 4 else "C",
                 "participant": p, "mean_score": mean(reports, p),
                 "verdict_note": any(s.get("hard_requirement_fail") for s in [verdict]) and any(
                     d["participant"] == p and d.get("hard_requirement_fail") for d in verdict.get("ranking", []))}
        ranks.append(entry)
    open(os.path.join(RES, "winner.json"), "w").write(json.dumps(
        {"winner": verdict.get("winner"), "tiers": ranks, "reason": verdict.get("reason")}, indent=2))
    lines = ["# Tier list\n\n| Tier | Participant | Mean |", "|---|---|---|"]
    lines += [f"| {r['tier']} | {r['participant']} | {r['mean_score']} |" for r in ranks]
    open(os.path.join(RES, "tierlist.md"), "w").write("\n".join(lines) + "\n")
    for p in PARTS:
        rows = scores_of(reports).get(p, [])
        body = [f"# {p}\n\nMean summary: {mean(reports, p)}\n"]
        for jid, s in rows:
            body.append(f"## {jid}\n```json\n{json.dumps(s, ensure_ascii=False, indent=1)}\n```\n")
            for c in CRIT:
                v = s.get("criteria", {}).get(c)
                if v is not None:
                    body.append(f"- {c}: {v}")
            body.append(f"- notes: {s.get('notes','')}")
        open(os.path.join(RES, f"analytics-{p}.md"), "w").write("\n".join(body) + "\n")


if __name__ == "__main__":
    reports = [json.load(open(os.path.join(RES, f"judge{i}.json"))) for i in (1, 2, 3)]
    verdict, agree = final_round(reports, "r1")
    if agree < 2:
        print(f"Disagreement ({agree}/3 agree) -> rerun scoring round")
        rerun_judges()
        recent = [json.load(open(os.path.join(RES, f"judge{i}.json"))) for i in (1, 2, 3)]
        verdict, agree = final_round(recent, "r2")
        reports = recent
    artifacts(reports, verdict)
    print("Winner:", verdict.get("winner"), "| votes agreed:", agree)
