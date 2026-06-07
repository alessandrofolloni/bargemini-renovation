<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import { useRouter } from 'vue-router'
import logoImg from '../assets/logo_original.jpg'

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()

onMounted(() => {
  if (localStorage.getItem('token')) router.push('/admin')
})

const handleLogin = async () => {
  error.value = ''
  loading.value = true
  try {
    const params = new URLSearchParams()
    params.append('username', username.value)
    params.append('password', password.value)
    const { data } = await api.post('/token', params)
    localStorage.setItem('token', data.access_token)
    router.push('/admin')
  } catch (err) {
    error.value =
      err.response?.status === 401
        ? 'Nome utente o password errati. Riprova.'
        : 'Errore di connessione. Il backend è attivo?'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-card">
      <img :src="logoImg" alt="Bar Gemini" class="login-logo" />
      <span class="eyebrow">Portale Staff</span>
      <h1>Accesso riservato</h1>
      <p class="login-sub">Inserisci le credenziali per gestire prenotazioni e menu.</p>

      <form class="login-form" @submit.prevent="handleLogin">
        <div class="field">
          <label>Nome utente</label>
          <input v-model="username" type="text" required placeholder="admin" autocomplete="username" />
        </div>
        <div class="field">
          <label>Password</label>
          <input v-model="password" type="password" required placeholder="••••••••" autocomplete="current-password" />
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <button type="submit" class="btn btn-primary full" :disabled="loading">
          {{ loading ? 'Accesso in corso…' : 'Accedi' }}
        </button>
      </form>

      <router-link to="/" class="back">← Torna al sito</router-link>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
  background:
    radial-gradient(circle at 20% 20%, rgba(181, 58, 43, 0.08), transparent 40%),
    radial-gradient(circle at 80% 80%, rgba(193, 152, 78, 0.1), transparent 45%),
    var(--bg-white);
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: 48px 44px;
  text-align: center;
}

.login-logo {
  height: 56px;
  width: auto;
  margin: 0 auto 22px;
  border-radius: 10px;
  box-shadow: var(--shadow-soft);
}

.login-card h1 {
  font-size: 1.8rem;
  margin: 8px 0 8px;
}

.login-sub {
  color: var(--text-soft);
  font-size: 0.95rem;
  margin-bottom: 34px;
}

.login-form {
  text-align: left;
  display: grid;
  gap: 18px;
}

.field label {
  display: block;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--secondary);
  margin-bottom: 8px;
}

.field input {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--bg-white);
  font-family: var(--font-sans);
  font-size: 1rem;
  color: var(--text-main);
  transition: border-color 0.25s ease, box-shadow 0.25s ease;
}

.field input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(181, 58, 43, 0.12);
}

.full {
  width: 100%;
  margin-top: 6px;
}

.error {
  color: var(--primary);
  font-size: 0.88rem;
  font-weight: 600;
  margin: -2px 0 0;
}

.back {
  display: inline-block;
  margin-top: 28px;
  color: var(--text-soft);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
  transition: color 0.2s ease;
}

.back:hover {
  color: var(--primary);
}
</style>
