<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import QrcodeVue from 'qrcode.vue'
import logoImg from './assets/logo_original.jpg'

const showQR = ref(false)
const route = useRoute()

const isStaffPage = computed(() => {
  return ['/login', '/admin'].includes(route.path)
})

const isAuthenticated = computed(() => {
  return !!localStorage.getItem('token')
})
</script>

<template>
  <div class="app-shell">
    <!-- Shared Header - Hidden on staff pages -->
    <header v-if="!isStaffPage" class="site-header">
      <div class="container header-inner">
        <router-link to="/" class="brand-container">
          <div class="logo-wrapper">
            <img :src="logoImg" alt="Bar Gemini" class="header-logo" />
          </div>
          <div class="brand-text">
            <span class="brand-main">GEMINI</span>
            <span class="brand-sub">DAL 1990</span>
          </div>
        </router-link>
        
        <nav class="main-nav">
          <router-link to="/menu" class="nav-link">Menu</router-link>
          <router-link to="/about" class="nav-link">Storia</router-link>
          <router-link to="/reservation" class="nav-cta-premium">Prenota</router-link>
        </nav>

        <div class="header-tools">
          <button @click="showQR = true" class="qr-btn-minimal">
            <span class="qr-icon">📱</span>
            <span class="qr-text">Menu Digitale</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Page Content -->
    <main :class="{ 'staff-buffer': isStaffPage }">
      <router-view></router-view>
    </main>

    <!-- Shared Footer - Hidden on staff pages -->
    <footer v-if="!isStaffPage" class="site-footer">
      <div class="container footer-grid">
        <div class="footer-col">
          <span class="footer-brand">BAR GEMINI.</span>
          <p class="footer-desc">
            Un'istituzione senza tempo a Reggio Emilia dal 1990.
            Dove la tradizione italiana incontra la moderna ospitalità.
          </p>
        </div>
        
        <div class="footer-col">
          <h4>Trovaci</h4>
          <div class="footer-contact">
            <p>Via Aristotele, 102<br>Reggio Emilia, Italia</p>
            <p><a href="tel:+390522123456">+39 0522 123456</a></p>
          </div>
        </div>

        <div class="footer-col footer-links">
          <h4>Contatti</h4>
          <div class="footer-contact">
            <p><a href="https://instagram.com" target="_blank">Instagram</a></p>
            <p><a href="mailto:info@bargemini.it">info@bargemini.it</a></p>
            <router-link v-if="!isAuthenticated" to="/login" class="staff-access">Accesso Staff</router-link>
            <router-link v-else to="/admin" class="staff-access dashboard-hint">Dashboard Admin →</router-link>
          </div>
        </div>
      </div>
    </footer>

    <!-- QR Modal -->
    <div v-if="showQR" class="qr-overlay" @click="showQR = false">
      <div class="qr-modal-body" @click.stop>
        <button class="close-qr" @click="showQR = false">×</button>
        <h3>Menu Digitale</h3>
        <qrcode-vue value="http://bargemini.it/menu" :size="200" level="H" />
        <p>Scansiona per esplorare la nostra selezione</p>
      </div>
    </div>
  </div>
</template>

<style>
/* Global Layout Styles */
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex-grow: 1;
}

/* Header */
.site-header {
  position: fixed;
  top: 20px; 
  left: 20px; 
  right: 20px;
  height: 90px;
  background: var(--glass);
  backdrop-filter: blur(25px);
  z-index: 1000;
  display: flex;
  align-items: center;
  border-radius: var(--radius-md);
  border: 1px solid var(--glass-border);
  box-shadow: var(--shadow-md);
  transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.header-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.brand-container {
  display: flex;
  align-items: center;
  text-decoration: none;
  gap: 15px;
}

.logo-wrapper {
  background: white;
  padding: 5px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
  display: flex;
  align-items: center;
  transition: transform 0.3s ease;
}

.brand-container:hover .logo-wrapper {
  transform: scale(1.05) rotate(-2deg);
}

.header-logo {
  height: 55px;
  width: auto;
  display: block;
}

.brand-text {
  display: flex;
  flex-direction: column;
  line-height: 1;
}

.brand-main {
  font-family: var(--font-serif);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--secondary);
  letter-spacing: -0.5px;
}

.brand-sub {
  font-family: var(--font-sans);
  font-size: 0.6rem;
  font-weight: 700;
  color: var(--primary);
  letter-spacing: 2px;
  text-transform: uppercase;
}

.main-nav {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-link {
  text-decoration: none;
  color: var(--secondary);
  padding: 8px 12px;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.3s;
  position: relative;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: var(--primary);
  transition: all 0.3s;
  transform: translateX(-50%);
}

.nav-link:hover::after, .nav-link.router-link-active::after {
  width: 80%;
}

.nav-link:hover, .nav-link.router-link-active {
  color: var(--primary);
  background: none;
}

.nav-cta-premium {
  background: var(--secondary);
  color: #fff !important;
  padding: 12px 28px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 15px rgba(44, 62, 80, 0.3);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.nav-cta-premium:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(44, 62, 80, 0.4);
  background: var(--primary);
}

.qr-btn-minimal {
  background: rgba(255,255,255,0.8);
  border: 1px solid var(--border);
  padding: 10px 20px;
  border-radius: 50px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: all 0.3s;
  backdrop-filter: blur(10px);
}

.qr-btn-minimal:hover {
  border-color: var(--secondary);
  transform: scale(1.02);
}

.qr-text {
  font-weight: 700;
  font-size: 0.8rem;
  color: var(--secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* Footer Architecture */
.site-footer {
  padding: 100px 0 60px;
  background: var(--secondary);
  color: white;
  margin-top: 120px;
  position: relative;
  overflow: hidden;
}

.site-footer::before {
  content: "BAR GEMINI";
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 15rem;
  font-family: var(--font-serif);
  color: rgba(255,255,255,0.03);
  white-space: nowrap;
  pointer-events: none;
  font-weight: 700;
}

.footer-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 60px;
  align-items: start;
  position: relative;
  z-index: 2;
}

.footer-brand {
  font-family: var(--font-serif);
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 20px;
  display: block;
  letter-spacing: -1px;
}

.footer-desc {
  color: rgba(255,255,255,0.6);
  font-size: 1rem;
  max-width: 300px;
  line-height: 1.6;
}

.footer-col h4 {
  color: var(--primary); /* Gold/Primary accent */
  font-family: var(--font-sans);
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 25px;
}

.footer-contact p {
  color: rgba(255,255,255,0.8);
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.footer-contact a {
  color: white;
  text-decoration: none;
  border-bottom: 1px solid rgba(255,255,255,0.3);
  padding-bottom: 2px;
  transition: border-color 0.3s;
}

.footer-contact a:hover {
  border-color: var(--primary);
}

.footer-links {
  text-align: right;
}

.staff-access {
  color: rgba(255,255,255,0.4);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s;
}

.staff-access:hover {
  color: white;
}

@media (max-width: 768px) {
  .footer-grid { grid-template-columns: 1fr; gap: 40px; }
  .footer-links { text-align: left; }
  .site-footer::before { font-size: 8rem; }
}

/* QR Modal */
.qr-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.9);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qr-modal-body {
  background: #fff;
  padding: 80px;
  position: relative;
  text-align: center;
  border-radius: var(--radius-lg);
}

.close-qr {
  position: absolute;
  top: 20px; right: 20px;
  font-size: 2rem;
  background: none; border: none;
  cursor: pointer;
}
</style>
