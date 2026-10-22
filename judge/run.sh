#!/usr/bin/env sh
# Hackathon scoring orchestrator.
# Usage: sh judge/run.sh
# Requires: opencode CLI, local LLM on :8000 (the judged sites target it).
# Judge/final model ids changed via env: J1= J2= J3= FINAL=

set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
RES=$ROOT/judge/results
mkdir -p "$RES"
cd "$ROOT"

J1=${J1:-opencode-go/glm-5.3-flash}
J2=${J2:-opencode-go/mimo-v2.6-flash}
J3=${J3:-opencode-go/qwen3.7-plus}
FINAL=${FINAL:-opencode-go/minimax-m3}
PROMPT=$(cat judge/evaluator-prompt.md)

judge() { # $1 model, $2 name
  echo "== judging with $2 ($1): $(date)" | tee "$RES/log-$2.txt"
  opencode run --model "$1" -- "$PROMPT" 2>&1 | tee -a "$RES/log-$2.txt"
}

extract_json() { # $1 raw log, $2 out.json — pull first valid JSON object from agent answer
  python3 - "$1" "$2" <<'EOF'
import json,sys
raw=open(sys.argv[1]).read()
dec=json.JSONDecoder()
best=None
i=raw.find('{')
while i!=-1:
    try:
        obj,_=dec.raw_decode(raw[i:])
    except json.JSONDecodeError:
        pass
    else:
        if isinstance(obj,dict) and 'scores' in obj:
            best=obj
    i=raw.find('{',i+1)
assert best is not None, 'no scores JSON found'
open(sys.argv[2],'w').write(json.dumps(best,ensure_ascii=False,indent=2))
EOF
}

rm -f "$RES"/log-judge{1,2,3}.txt
judge "$J1" judge1 & P1=$!
judge "$J2" judge2 & P2=$!
judge "$J3" judge3 & P3=$!
echo "Judges running in parallel — watch: tail -f judge/results/log-judge{1,2,3}.txt"
wait $P1; S1=$?; wait $P2; S2=$?; wait $P3; S3=$?
echo "Judge exit codes: $S1 $S2 $S3"
extract_json "$RES/log-judge1.txt" "$RES/judge1.json"
extract_json "$RES/log-judge2.txt" "$RES/judge2.json"
extract_json "$RES/log-judge3.txt" "$RES/judge3.json"

python3 judge/pipeline.py "$RES" "$FINAL"
