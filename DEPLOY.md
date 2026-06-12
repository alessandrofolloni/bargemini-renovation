# Andare in produzione — guida

Il sito è un'unica app: il backend FastAPI serve anche il sito Vue già
compilato, quindi gira tutto su **una sola porta / un solo indirizzo**.

---

## ✅ Checklist prima di pubblicare (lato tuo)

1. **Segreti** — in `backend/.env` (parti da `backend/.env.example`):
   - `SECRET_KEY` → stringa lunga e casuale: `openssl rand -hex 32`
   - `ADMIN_PASSWORD` → password forte (l'utente resta `admin`)
   - `ALLOW_ORIGINS` → il tuo dominio, es. `https://www.bargemini.it`
2. **Contatti reali** — modifica **un solo file**: `frontend/src/config.js`
   (telefono, indirizzo, email, Instagram, link Maps, mappa, orari, P.IVA).
3. **Foto e menu** — sostituisci le immagini in `frontend/src/assets/` con foto
   reali del bar; verifica/aggiorna i piatti e i prezzi dal pannello admin.
4. **Email** (facoltativo) — per inviare le email di conferma ai clienti, metti
   credenziali SMTP reali in `.env` (per Gmail serve una *App Password*). Se le
   lasci coi valori d'esempio, il sito non invia nulla (nessun errore).
5. **Legale** — rivedi i testi in `frontend/src/views/Privacy.vue` e aggiungi la
   P.IVA in `config.js`. Il consenso privacy e il banner cookie sono già attivi.

All'avvio il server stampa un avviso per ogni impostazione ancora insicura.

---

## Opzione A — Mostrarlo al volo (link temporaneo)

```bash
./share.sh
```

Crea un link pubblico `https://….trycloudflare.com` valido finché il tuo PC è
acceso e lo script è in esecuzione. Ottimo per una demo, non per la produzione.

---

## Opzione B — Online stabilmente (Docker)

L'app è pacchettizzata in un `Dockerfile`. L'immagine compila il frontend e
serve sito + API sulla porta **8000**.

**Provala in locale:**

```bash
docker build -t bargemini .
docker run -p 8000:8000 --env-file backend/.env bargemini
# apri http://localhost:8000
```

**Dati persistenti (importante):** il database è un file SQLite. Per non perdere
le prenotazioni a ogni riavvio, monta un volume e punta `DATABASE_PATH` lì:

```bash
docker run -p 8000:8000 \
  --env-file backend/.env \
  -e DATABASE_PATH=/data/bargemini.db \
  -v bargemini_data:/data \
  bargemini
```

### Su un hosting

Qualsiasi host che esegue immagini Docker va bene. In tutti i casi:

- imposta le **variabili d'ambiente** del file `.env` nel pannello dell'host
  (non caricare il file `.env` nel repository);
- imposta `DATABASE_PATH=/data/bargemini.db` e collega un **volume/disco
  persistente** montato su `/data`;
- l'host fornirà **HTTPS** e un dominio automaticamente.

**Esempio con Fly.io** (ha i volumi nativi):

```bash
fly launch --no-deploy            # genera fly.toml, porta interna 8000
fly volume create bargemini_data --size 1
fly secrets set SECRET_KEY=... ADMIN_PASSWORD=... ALLOW_ORIGINS=https://tuodominio \
              DATABASE_PATH=/data/bargemini.db
# in fly.toml: [[mounts]] source="bargemini_data" destination="/data"
fly deploy
```

(Stesso schema su Railway, Render con un *Disk*, o un piccolo VPS.)

---

## Dopo il primo avvio
- Vai su `/login` e accedi con le credenziali impostate.
- Da **Gestione Menu** carica/aggiorna i piatti (anche con l'importazione rapida).
- Fai una prenotazione di prova per verificare il flusso completo.
