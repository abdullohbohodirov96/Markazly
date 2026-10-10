#!/usr/bin/env bash
# Barcha testlarni ishga tushiradi: har bir server testi uchun toza bazali server ko'tariladi.
# Foydalanish: bash scripts/test-all.sh [test-nomi ...]
cd "$(dirname "$0")/.."
# Testlar hamma modul yoqilgan sinov sozlamasi bilan ishlaydi
export MARKAZ_FILE="$PWD/tests/markaz.test.json"
PASS='Albyana2026!'
# Sinov uchun index.html Google Analytics tegi bilan quriladi (site-test GA himoyasini tekshiradi); oxirida qayta quriladi
GA_MEASUREMENT_ID=G-SINOV0000 node build.js >/dev/null
trap 'MARKAZ_FILE= node build.js >/dev/null' EXIT
TMP=$(mktemp -d)
RES="$TMP/natija.txt"; : > "$RES"
UNIT="game-test run-tests backup-test bot-admin-test bot-idle-test bot-reg-test bot-test kabinet-bot-test kanal-quiz-test link-test paybot-test tozalash-test seo-render-test kod-test lms-test level-test"
ALL=${*:-$(ls tests/*.js | xargs -n1 basename | sed 's/\.js$//')}
port=3500
for t in $ALL; do
  case " db-test restore-test perf-test " in *" $t "*) echo "SKIP $t" >> "$RES"; continue;; esac
  if [[ " $UNIT " == *" $t "* ]]; then
    timeout 200 node tests/$t.js > "$TMP/$t.log" 2>&1; rc=$?
  else
    port=$((port+1)); d="$TMP/data_$t"; mkdir -p "$d"
    TRUST_PROXY_HOPS=$([ "$t" = hujum2-test ] && echo 1 || echo 0) FLOOD_MAX=$([ "$t" = toshqin-test ] && echo 50 || echo "${FLOOD_MAX_DEF:-}") PORT=$port DATA_DIR=$d BACKUP_DIR=$d/bk SEED_DIRECTOR_PASSWORD="$PASS" NODE_ENV=test \
      node server/index.js > "$TMP/$t.server.log" 2>&1 & sp=$!
    for i in $(seq 1 50); do curl -s -o /dev/null localhost:$port/api/health && break; sleep 0.2; done
    ARG1=$port; [ "$t" = daraja-ui-test ] && ARG1="http://localhost:$port/"
    timeout 200 node tests/$t.js $ARG1 "$PASS" > "$TMP/$t.log" 2>&1; rc=$?
    kill $sp 2>/dev/null; wait $sp 2>/dev/null
  fi
  summ=$(grep -aE "o'tdi|o’tdi|passed|✓|✗|FAIL|Xato" "$TMP/$t.log" | tail -1 | cut -c1-120)
  echo "$([ $rc = 0 ] && echo OK || echo "FAIL($rc)") $t :: $summ" >> "$RES"
done
cat "$RES"; echo "LOGS: $TMP"
