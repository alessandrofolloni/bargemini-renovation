<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()

onMounted(() => {
  // If already logged in, skip to dashboard
  if (localStorage.getItem('token')) {
    router.push('/admin')
  }
})

const handleLogin = async () => {
  error.value = ''
  loading.value = true
  
  try {
    const params = new URLSearchParams()
    params.append('username', username.value)
    params.append('password', password.value)
    
    const response = await api.post('/token', params)
    localStorage.setItem('token', response.data.access_token)
    router.push('/admin')
  } catch (err) {
    if (err.response?.status === 401) {
      error.value = 'Nome utente o password errati. Riprova.'
    } else {
      error.value = 'Errore di connessione. Il backend è attivo?'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-card animate-fade">
      <div class="logo">GEMINI <span class="accent">STAFF</span></div>
      <h2>Accesso Ufficio Interno</h2>
      <p class="subtitle">Inserisci le tue credenziali per gestire le prenotazioni.</p>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="input-group">
          <label>Nome Utente</label>
          <input v-model="username" type="text" required placeholder="Es: admin" />
        </div>
        <div class="input-group">
          <label>Password</label>
          <input v-model="password" type="password" required placeholder="••••••••" />
        </div>
        
        <p v-if="error" class="error-msg">{{ error }}</p>
        
        <button type="submit" class="btn-primary-solid full-width" :disabled="loading">
          {{ loading ? 'Accesso in corso...' : 'Accedi' }}
        </button>
      </form>
      
      <router-link to="/" class="back-link">← Torna al Sito</router-link>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f6f7; /* Matching original site light grey */
}

.login-card {
  width: 100%;
  max-width: 420px;
  padding: 50px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  text-align: center;
  border: 1px solid #eee;
}

.logo { 
  font-size: 1.5rem; 
  font-weight: 800; 
  margin-bottom: 20px;
  color: #333;
}

.accent { color: var(--primary); }

h2 { font-size: 1.5rem; margin-bottom: 5px; color: #1a1a1a; }
.subtitle { color: #666; font-size: 0.9rem; margin-bottom: 40px; }

.login-form { text-align: left; }

.input-group { margin-bottom: 20px; }

label { 
  display: block; 
  margin-bottom: 8px; 
  color: #444; 
  font-size: 0.85rem; 
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

input {
  width: 100%;
  background: #fcfcfc;
  border: 1px solid #ddd;
  padding: 14px;
  border-radius: 4px;
  color: #333;
  box-sizing: border-box;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: var(--secondary);
}

.btn-primary-solid {
  background: var(--primary);
  color: white;
  border: none;
  padding: 16px;
  border-radius: 4px;
  font-weight: 700;
  cursor: pointer;
  font-size: 1rem;
  margin-top: 10px;
  transition: opacity 0.2s;
}

.btn-primary-solid:disabled { opacity: 0.6; cursor: not-allowed; }

.error-msg { color: #e74c3c; font-size: 0.85rem; margin-bottom: 15px; font-weight: 600; }

.back-link {
  display: block;
  margin-top: 30px;
  color: var(--secondary);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
}
</style>
