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
</script>

<template>
  <div class="app-shell">
    <!-- Shared Header - Hidden on staff pages -->
    <header v-if="!isStaffPage" class="site-header">
      <div class="container header-inner">
        <router-link to="/" class="brand">
          <img :src="logoImg" alt="Bar Gemini" class="header-logo" />
        </router-link>
        <nav class="main-nav">
          <router-link to="/menu">Menu</router-link>
          <router-link to="/about">Story</router-link>
          <router-link to="/reservation" class="nav-cta">Reserve</router-link>
        </nav>
        <button @click="showQR = true" class="qr-trigger">QR Menu</button>
      </div>
    </header>

    <!-- Page Content -->
    <main :class="{ 'staff-buffer': isStaffPage }">
      <router-view></router-view>
    </main>

    <!-- Shared Footer - Hidden on staff pages -->
    <footer v-if="!isStaffPage" class="site-footer">
      <div class="container footer-grid">
        <div class="footer-brand">BAR GEMINI.</div>
        <div class="footer-copy">© 2026 Crafted for the modern palate.</div>
        <div class="footer-links">
          <router-link to="/login" class="staff-access">Staff Login</router-link>
        </div>
      </div>
    </footer>

    <!-- QR Modal -->
    <div v-if="showQR" class="qr-overlay" @click="showQR = false">
      <div class="qr-modal-body" @click.stop>
        <button class="close-qr" @click="showQR = false">×</button>
        <h3>Digital Menu</h3>
        <qrcode-vue value="http://bargemini.it/menu" :size="200" level="H" />
        <p>Scan to explore our full selection</p>
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
  top: 0; left: 0; right: 0;
  height: 100px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  z-index: 1000;
  display: flex;
  align-items: center;
  border-bottom: 1px solid var(--border);
}

.header-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.brand {
  display: flex;
  align-items: center;
  text-decoration: none;
}

.header-logo {
  height: 60px;
  width: auto;
  border-radius: 4px;
}

.accent {
  color: var(--primary);
}

.main-nav a {
  text-decoration: none;
  color: var(--text-main);
  margin: 0 20px;
  font-weight: 600;
  font-size: 0.9rem;
  transition: color 0.3s;
}

.main-nav a:hover, .main-nav a.router-link-active {
  color: var(--primary);
}

.nav-cta {
  background: var(--text-main);
  color: #fff !important;
  padding: 10px 25px;
  border-radius: var(--radius-sm);
}

.qr-trigger {
  background: none;
  border: 1px solid var(--border);
  padding: 8px 15px;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: 0.8rem;
}

/* Footer */
.site-footer {
  padding: 60px 0;
  background: var(--bg-soft);
  border-top: 1px solid var(--border);
  margin-top: 80px;
}

.footer-grid {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-brand {
  font-weight: 800;
  font-size: 1.2rem;
}

.footer-copy {
  color: var(--text-soft);
  font-size: 0.9rem;
}

.staff-access {
  color: var(--text-soft);
  text-decoration: none;
  font-size: 0.8rem;
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
