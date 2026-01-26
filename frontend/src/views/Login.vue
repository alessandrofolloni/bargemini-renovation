<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const handleLogin = async () => {
  try {
    const formData = new FormData()
    formData.append('username', username.value)
    formData.append('password', password.value)
    
    const response = await axios.post('http://localhost:8000/token', formData)
    localStorage.setItem('token', response.data.access_token)
    router.push('/admin')
  } catch (err) {
    error.value = 'Invalid credentials'
  }
}
</script>

<template>
  <div class="login-page">
    <div class="glass-card login-card animate-fade">
      <div class="logo">GEMINI <span class="highlight">STAFF</span></div>
      <h2>Internal Access</h2>
      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label>Username</label>
          <input v-model="username" type="text" required />
        </div>
        <div class="input-group">
          <label>Password</label>
          <input v-model="password" type="password" required />
        </div>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <button type="submit" class="btn-primary full-width">Sign In</button>
      </form>
      <router-link to="/" class="back-link">← Back to Site</router-link>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle at center, #1a1a1a 0%, #000 100%);
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 3rem;
  text-align: center;
}

.logo { font-size: 1.5rem; font-weight: 700; margin-bottom: 2rem; }

.input-group {
  text-align: left;
  margin-bottom: 1.5rem;
}

label { display: block; margin-bottom: 0.5rem; color: var(--text-muted); font-size: 0.9rem; }

input {
  width: 100%;
  background: rgba(255,255,255,0.05);
  border: 1px solid var(--glass-border);
  padding: 0.8rem;
  border-radius: 8px;
  color: white;
  box-sizing: border-box;
}

.error-msg { color: #ff5555; font-size: 0.9rem; margin-bottom: 1rem; }

.back-link {
  display: block;
  margin-top: 2rem;
  color: var(--text-muted);
  text-decoration: none;
  font-size: 0.9rem;
}
</style>
