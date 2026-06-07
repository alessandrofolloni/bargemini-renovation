#!/bin/bash
#
# Share Bar Gemini with anyone via a temporary public link.
# Builds the site, serves it together with the API on one port, and opens a
# free Cloudflare quick-tunnel (no account needed). Keep this window open while
# you want the link to stay live; press Ctrl+C to stop.
#
set -e
cd "$(dirname "$0")"

echo "🏗️  Compilazione del sito..."
( cd frontend && npm run build >/dev/null 2>&1 )
echo "✅ Sito compilato."

echo "📡 Avvio del server (sito + API insieme su :8000)..."
cd backend
[ -d venv ] && source venv/bin/activate
python3 main.py > /tmp/bargemini_backend.log 2>&1 &
BACKEND_PID=$!
cd ..

cleanup() { echo ""; echo "🛑 Chiusura..."; kill "$BACKEND_PID" 2>/dev/null; exit; }
trap cleanup SIGINT SIGTERM

sleep 3
if ! curl -s -o /dev/null http://localhost:8000/api/menu; then
  echo "❌ Il server non è partito. Controlla /tmp/bargemini_backend.log"
  cleanup
fi

if ! command -v cloudflared >/dev/null 2>&1; then
  echo ""
  echo "⚠️  Per creare il link pubblico serve 'cloudflared' (gratuito, senza account)."
  echo "    Installalo una volta sola con:"
  echo ""
  echo "        brew install cloudflared"
  echo ""
  echo "    Poi rilancia:  ./share.sh"
  echo ""
  echo "👉 Intanto il sito è visibile sul tuo computer: http://localhost:8000"
  echo "   (Premi Ctrl+C per fermare.)"
  wait "$BACKEND_PID"
  exit 0
fi

echo ""
echo "🌍 Creazione del link pubblico... copia l'indirizzo https://....trycloudflare.com qui sotto"
echo "   e invialo a chi vuoi. Lascia questa finestra aperta. (Ctrl+C per fermare.)"
echo ""
cloudflared tunnel --url http://localhost:8000
cleanup
