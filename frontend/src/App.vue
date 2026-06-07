<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import QrcodeVue from 'qrcode.vue'
import logoImg from './assets/logo_original.jpg'

const showQR = ref(false)
const scrolled = ref(false)
const route = useRoute()

const isStaffPage = computed(() => ['/login', '/admin'].includes(route.path))
const isAuthenticated = computed(() => !!localStorage.getItem('token'))

const onScroll = () => { scrolled.value = window.scrollY > 24 }
onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

const year = new Date().getFullYear()
</script>

<template>
  <div class="app-shell">
    <!-- Header — hidden on staff pages -->
    <header v-if="!isStaffPage" class="site-header" :class="{ scrolled }">
      <div class="container header-inner">
        <router-link to="/" class="brand">
          <img :src="logoImg" alt="Bar Gemini" class="brand-logo" />
          <span class="brand-text">
            <span class="brand-main">Gemini</span>
            <span class="brand-sub">Caffè · dal 1990</span>
          </span>
        </router-link>

        <nav class="main-nav">
          <router-link to="/menu" class="nav-link">Menu</router-link>
          <router-link to="/about" class="nav-link">Storia</router-link>
          <button @click="showQR = true" class="nav-link nav-qr">Menu Digitale</button>
          <router-link to="/reservation" class="btn btn-primary nav-cta">Prenota</router-link>
        </nav>
      </div>
    </header>

    <!-- Page content -->
    <main>
      <router-view />
    </main>

    <!-- Footer — hidden on staff pages -->
    <footer v-if="!isStaffPage" class="site-footer">
      <div class="container">
        <div class="footer-grid">
          <div class="footer-brand-col">
            <span class="footer-brand">Bar Gemini</span>
            <p class="footer-desc">
              Un'istituzione senza tempo a Reggio Emilia dal 1990. Dove la
              tradizione italiana incontra la moderna ospitalità.
            </p>
            <div class="footer-social">
              <a href="https://instagram.com" target="_blank" rel="noopener">Instagram</a>
              <a href="mailto:info@bargemini.it">Email</a>
            </div>
          </div>

          <div class="footer-col">
            <h4>Dove</h4>
            <p>Via Aristotele, 102<br />42122 Reggio Emilia (RE)</p>
            <a href="tel:+390522123456" class="footer-link">+39 0522 123456</a>
          </div>

          <div class="footer-col">
            <h4>Orari</h4>
            <p>Lun–Ven&nbsp;&nbsp;07:00 – 21:00<br />Sabato&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;08:00 – 24:00<br />Domenica&nbsp;&nbsp;Chiuso</p>
          </div>

          <div class="footer-col">
            <h4>Vai a</h4>
            <router-link to="/menu" class="footer-link">Menu</router-link>
            <router-link to="/reservation" class="footer-link">Prenota un tavolo</router-link>
            <router-link to="/about" class="footer-link">La nostra storia</router-link>
          </div>
        </div>

        <div class="footer-bottom">
          <span>© {{ year }} Bar Gemini — Reggio Emilia</span>
          <router-link v-if="!isAuthenticated" to="/login" class="staff-access">Accesso Staff</router-link>
          <router-link v-else to="/admin" class="staff-access">Dashboard Admin →</router-link>
        </div>
      </div>
    </footer>

    <!-- QR modal -->
    <transition name="fade">
      <div v-if="showQR" class="qr-overlay" @click="showQR = false">
        <div class="qr-modal" @click.stop>
          <button class="close-qr" @click="showQR = false" aria-label="Chiudi">×</button>
          <span class="eyebrow">Menu Digitale</span>
          <h3>Inquadra & scopri</h3>
          <div class="qr-frame">
            <qrcode-vue value="http://bargemini.it/menu" :size="190" level="H" />
          </div>
          <p>Scansiona con la fotocamera per sfogliare la nostra selezione.</p>
        </div>
      </div>
    </transition>
  </div>
</template>

<style>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex-grow: 1;
}

/* ---- Header ---- */
.site-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 84px;
  z-index: 1000;
  display: flex;
  align-items: center;
  transition: background 0.4s ease, box-shadow 0.4s ease, border-color 0.4s ease, height 0.4s ease;
  border-bottom: 1px solid transparent;
}

.site-header.scrolled {
  height: 72px;
  background: rgba(246, 241, 234, 0.82);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom-color: var(--border);
  box-shadow: 0 6px 24px rgba(40, 26, 14, 0.05);
}

.header-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  display: flex;
  align-items: center;
  gap: 14px;
  text-decoration: none;
}

.brand-logo {
  height: 46px;
  width: auto;
  border-radius: 9px;
  box-shadow: var(--shadow-soft);
  background: #fff;
  padding: 3px;
}

.brand-text {
  display: flex;
  flex-direction: column;
  line-height: 1.05;
}

.brand-main {
  font-family: var(--font-serif);
  font-size: 1.45rem;
  font-weight: 700;
  color: var(--secondary);
}

.brand-sub {
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--primary);
}

.main-nav {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-link {
  font-family: var(--font-sans);
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--secondary);
  text-decoration: none;
  padding: 10px 16px;
  border: none;
  background: none;
  cursor: pointer;
  border-radius: var(--radius-pill);
  transition: color 0.25s ease, background 0.25s ease;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--primary);
}

.nav-qr {
  position: relative;
}

.nav-cta {
  margin-left: 10px;
  padding: 12px 26px;
  font-size: 0.9rem;
}

/* ---- Footer ---- */
.site-footer {
  background: var(--secondary);
  color: rgba(255, 255, 255, 0.75);
  padding: 90px 0 36px;
  margin-top: 120px;
}

.footer-grid {
  display: grid;
  grid-template-columns: 1.6fr 1fr 1fr 1fr;
  gap: 50px;
  padding-bottom: 60px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-brand {
  font-family: var(--font-serif);
  font-size: 2rem;
  color: #fff;
  display: block;
  margin-bottom: 18px;
}

.footer-desc {
  max-width: 320px;
  line-height: 1.7;
  font-size: 0.98rem;
  margin-bottom: 24px;
}

.footer-social {
  display: flex;
  gap: 14px;
}

.footer-social a {
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #fff;
  text-decoration: none;
  padding: 8px 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--radius-pill);
  transition: all 0.25s ease;
}

.footer-social a:hover {
  background: var(--primary);
  border-color: var(--primary);
}

.footer-col h4 {
  color: var(--gold);
  font-family: var(--font-sans);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  margin-bottom: 20px;
}

.footer-col p {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.9;
  font-size: 0.98rem;
  margin-bottom: 14px;
}

.footer-link {
  display: block;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 0.98rem;
  margin-bottom: 10px;
  transition: color 0.25s ease;
  width: fit-content;
}

.footer-link:hover {
  color: #fff;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 28px;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.45);
}

.staff-access {
  color: rgba(255, 255, 255, 0.45);
  text-decoration: none;
  transition: color 0.25s ease;
}

.staff-access:hover {
  color: #fff;
}

@media (max-width: 900px) {
  .footer-grid {
    grid-template-columns: 1fr 1fr;
    gap: 40px;
  }
}

@media (max-width: 720px) {
  .main-nav {
    gap: 2px;
  }

  .nav-link {
    padding: 8px 10px;
    font-size: 0.85rem;
  }

  .nav-qr {
    display: none;
  }

  .brand-sub {
    display: none;
  }

  .footer-grid {
    grid-template-columns: 1fr;
  }

  .footer-bottom {
    flex-direction: column;
    gap: 12px;
  }
}

/* ---- QR modal ---- */
.qr-overlay {
  position: fixed;
  inset: 0;
  background: rgba(28, 20, 12, 0.6);
  backdrop-filter: blur(6px);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.qr-modal {
  background: var(--bg-surface);
  padding: 54px;
  position: relative;
  text-align: center;
  border-radius: var(--radius-lg);
  max-width: 380px;
  box-shadow: var(--shadow-hover);
}

.qr-modal h3 {
  font-size: 1.8rem;
  margin: 10px 0 26px;
}

.qr-frame {
  display: inline-flex;
  padding: 18px;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  margin-bottom: 22px;
}

.qr-modal p {
  color: var(--text-soft);
  font-size: 0.95rem;
  line-height: 1.6;
}

.close-qr {
  position: absolute;
  top: 18px;
  right: 22px;
  font-size: 1.8rem;
  line-height: 1;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-soft);
  transition: color 0.2s ease;
}

.close-qr:hover {
  color: var(--primary);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
