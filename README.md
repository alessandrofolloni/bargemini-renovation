# Bar Gemini Renovation

This project is a modern renovation of the Bar Gemini website, featuring a Python (FastAPI) backend and a Vue.js (Vite) frontend.

## Project Structure
- `/backend`: FastAPI Python application.
- `/frontend`: Vue.js 3 application with Vite.

## Backend (Python)
### Prerequisites
- Python 3.9+
- pip

### Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   python main.py
   ```
The API will be available at `http://localhost:8000`.

## Frontend (Vue.js)
### Prerequisites
- Node.js (Latest LTS recommended)
- npm or yarn

### Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
The website will be available at `http://localhost:5173`.

## Features
- **Editorial Design**: Warm "Italian caffè" visual system, fully responsive.
- **Dynamic Menu**: Fetched live from the FastAPI backend.
- **Reservations**: Table booking with optional dish pre-ordering (validated front and back).
- **Admin Dashboard**: Staff portal at `/login` to manage reservations and the menu.

## Managing the menu
Staff log in at `/login` → **Gestione Menu**. Dishes can be added, edited or
deleted one by one, and changes go live immediately on the public site.

For many dishes at once, use **⚡ Importazione rapida**: one dish per line as

```
Nome ; Prezzo ; Categoria ; Descrizione
```

e.g. `Tortelli Verdi ; 8.00 ; Primi ; Spinaci e ricotta, burro e salvia`.
You can also paste columns straight from Excel/Google Sheets (tab-separated).
Category is case-insensitive, incomplete lines are skipped.

## Configuration

### Backend (`backend/.env`)
| Variable | Purpose | Default |
| --- | --- | --- |
| `SECRET_KEY` | JWT signing key | `fallback-secret-key` |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` | Staff login credentials | `admin` / `bargemini2026` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime | `30` |
| `ALLOW_ORIGINS` | Comma-separated CORS origins | `*` |
| `SMTP_*` / `MAIL_FROM` | Reservation status emails (optional — logs a mock email if unset) | — |

> The default admin credentials are for local development only. Set a strong
> `SECRET_KEY` and `ADMIN_PASSWORD` before deploying — the server prints a
> warning on startup while defaults are in use.

### Security notes
- Passwords are stored **bcrypt-hashed** (never in plaintext); admin endpoints
  require a JWT obtained from `/token`.
- Reservations and menu items are **validated server-side** (email format, future
  date, phone, price ≥ 0, non-blank fields), so the API is safe even from direct calls.
- Before going live you should also: change `SECRET_KEY` and `ADMIN_PASSWORD`,
  restrict `ALLOW_ORIGINS` to your domain, and serve over **HTTPS**. For a public
  deployment consider adding rate-limiting on `/token`.

### Frontend
The backend URL is centralized in `frontend/src/api.js`. Override it at build
time with `VITE_API_URL` (defaults to `http://localhost:8000`).

## Quick Start
Run `./setup.sh` once to install dependencies, then `./start.sh` to launch both
servers (frontend on `:5173`, backend on `:8000`).

## Sharing the site (temporary demo link)
To show the site to someone who isn't with you, run:

```bash
./share.sh
```

It builds the site, serves it together with the API on a single port, and opens
a free **Cloudflare quick tunnel** that prints a public `https://….trycloudflare.com`
address — send that link to anyone. Keep the window open while you want it live;
press **Ctrl+C** to stop.

First time only, install the (free, no-account) tunnel tool:

```bash
brew install cloudflared
```

> The link is temporary and stays up only while `./share.sh` is running.

## Going to production
See **[DEPLOY.md](DEPLOY.md)** for the full checklist and a Docker-based deploy
with a persistent database. In short, before publishing you must: set real
secrets in `backend/.env` (copy from `backend/.env.example`), put the real
business details in `frontend/src/config.js`, replace the placeholder photos,
and review `frontend/src/views/Privacy.vue`.
