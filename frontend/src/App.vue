<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import QrcodeVue from 'qrcode.vue'
import logoImg from './assets/logo_original.jpg'

const showQR = ref(false)
const scrolled = ref(false)
const mobileOpen = ref(false)
const route = useRoute()

const isStaffPage = computed(() => ['/login', '/admin'].includes(route.path))
const isAuthenticated = computed(() => !!localStorage.getItem('token'))

const onScroll = () => { scrolled.value = window.scrollY > 24 }
onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

// Close the mobile menu whenever the route changes.
watch(route, () => { mobileOpen.value = false })

const year = new Date().getFullYear()

// QR points at the live site's own menu, so it works wherever the site is hosted.
const menuUrl = window.location.origin + '/menu'
</script>

<template>
  <div class="app-shell">
    <!-- Header — hidden on staff pages -->
    <header v-if="!isStaffPage" class="site-header" :class="{ scrolled, solid: mobileOpen }">
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

        <button
          class="burger"
          :class="{ open: mobileOpen }"
          @click="mobileOpen = !mobileOpen"
          :aria-expanded="mobileOpen"
          aria-label="Menu"
        >
          <span></span><span></span><span></span>
        </button>
      </div>

      <!-- Mobile dropdown -->
      <transition name="slide-down">
        <nav v-if="mobileOpen" class="mobile-nav">
          <router-link to="/menu" class="m-link">Menu</router-link>
          <router-link to="/about" class="m-link">Storia</router-link>
          <button class="m-link" @click="showQR = true; mobileOpen = false">Menu Digitale</button>
          <router-link to="/reservation" class="btn btn-primary m-cta">Prenota un tavolo</router-link>
        </nav>
      </transition>
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
            <qrcode-vue :value="menuUrl" :size="190" level="H" />
          </div>
          <p>Scansiona con la fotocamera per sfogliare la nostra selezione.</p>
          <a :href="menuUrl" class="qr-url">{{ menuUrl }}</a>
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

/* Burger (mobile only) */
.burger {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 44px;
  height: 44px;
  padding: 0;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--bg-surface);
  cursor: pointer;
}

.burger span {
  display: block;
  width: 20px;
  height: 2px;
  margin: 0 auto;
  background: var(--secondary);
  border-radius: 2px;
  transition: transform 0.3s ease, opacity 0.2s ease;
}

.burger.open span:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.burger.open span:nth-child(2) {
  opacity: 0;
}

.burger.open span:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

/* Mobile dropdown nav */
.mobile-nav {
  display: none;
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* ---- Footer ---- */
.site-footer {
  background: var(--secondary);
  color: rgba(255, 255, 255, 0.75);
  padding: 90px 0 36px;
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
  .site-header {
    height: 70px;
  }

  /* Always frost the header on mobile for legibility over content */
  .site-header,
  .site-header.scrolled {
    height: 70px;
    background: rgba(246, 241, 234, 0.92);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-bottom-color: var(--border);
  }

  .site-header.solid,
  .site-header.solid.scrolled {
    background: var(--bg-white);
  }

  .main-nav {
    display: none;
  }

  .burger {
    display: flex;
  }

  .brand-logo {
    height: 40px;
  }

  .mobile-nav {
    display: flex;
    flex-direction: column;
    gap: 4px;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    padding: 14px 22px 22px;
    background: var(--bg-white);
    border-bottom: 1px solid var(--border);
    box-shadow: var(--shadow-md);
  }

  .m-link {
    text-align: left;
    background: none;
    border: none;
    border-bottom: 1px solid var(--border);
    padding: 16px 4px;
    font-family: var(--font-sans);
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--secondary);
    text-decoration: none;
    cursor: pointer;
  }

  .m-link.router-link-active {
    color: var(--primary);
  }

  .m-cta {
    margin-top: 14px;
    width: 100%;
    padding: 16px;
    font-size: 1rem;
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

.qr-url {
  display: inline-block;
  margin-top: 12px;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--primary);
  text-decoration: none;
  word-break: break-all;
}

.qr-url:hover {
  text-decoration: underline;
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
