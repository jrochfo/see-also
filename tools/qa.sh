#!/bin/zsh
# Screenshot the local site for visual checks (needs `npm run dev` running on :8788 and Google Chrome).
#   tools/qa.sh "#art" light      -> tools/data/qa/art-light.png  (desktop 1300x800)
#   tools/qa.sh "#poetry" dark phone
# Headless Chrome follows the Mac's appearance; "light" forces light mode via a temporary copy of the page.
set -e
cd "${0:A:h}/.."
HASH=${1:-""}; THEME=${2:-device}; SIZE=${3:-desktop}
OUT=tools/data/qa; mkdir -p $OUT
NAME=$(echo "${HASH#\#}-$THEME-$SIZE" | tr '/' '-')
PAGE=index.html
if [[ $THEME == light ]]; then
  python3 -c "s=open('public/index.html').read();open('public/_qa.html','w').write(s.replace(\"document.documentElement.dataset.theme = t ||\",\"document.documentElement.dataset.theme = 'light' ||\"))"
  PAGE=_qa.html
fi
case $SIZE in phone) W=375,667;; ipad) W=820,1180;; *) W=1300,800;; esac
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars \
  --user-data-dir=$(mktemp -d) --window-size=$W --virtual-time-budget=15000 \
  --screenshot=$PWD/$OUT/$NAME.png "http://localhost:8788/$PAGE$HASH" >/dev/null 2>&1 || true
rm -f public/_qa.html
echo $OUT/$NAME.png
