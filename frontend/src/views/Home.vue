<script setup>
import interiorImg from '../assets/interior.png'
import coffeeImg from '../assets/coffee.png'
import pastriesImg from '../assets/pastries.png'
import aperitivoImg from '../assets/aperitivo_mock.png'
import { useScrollReveal } from '../composables/useScrollReveal'
import { site } from '../config'
import { cookieAccepted, acceptCookies } from '../consent'

useScrollReveal()

const features = [
  { img: coffeeImg, title: "Caffè d'Autore", text: 'Miscele tostate e preparate con cura, il modo perfetto per iniziare la giornata.' },
  { img: pastriesImg, title: 'Pasticceria Fresca', text: 'Delizie artigianali sfornate ogni mattina che si sciolgono in bocca.' },
  { img: aperitivoImg, title: 'Aperitivo & Cocktail', text: 'Il rito italiano per eccellenza, con spiriti selezionati e stuzzichini.' },
]

const services = [
  { icon: '🎟️', title: 'Ticket Restaurant', text: 'Accettiamo i principali buoni pasto per la pausa pranzo.' },
  { icon: '🚬', title: 'Tabacchi', text: 'Servizio tabaccheria e articoli per fumatori all\'interno.' },
  { icon: '🏧', title: 'Servizio ATM', text: 'Comodo prelievo contanti senza lasciare il bar.' },
  { icon: '🎰', title: 'Lotto & Giochi', text: 'Lotto, Superenalotto e Gratta e Vinci.' },
]
</script>

<template>
  <div class="home">
    <!-- Hero -->
    <section class="hero">
      <div class="container hero-grid">
        <div class="hero-text reveal">
          <span class="eyebrow">Caffetteria · Reggio Emilia · dal 1990</span>
          <h1>L'eccellenza<br />dell'<span class="accent">aperitivo</span>.</h1>
          <p class="lead">
            Lo storico ritrovo di Reggio Emilia, dove la passione per il caffè
            incontra l'arte del buon bere.
          </p>
          <div class="hero-actions">
            <router-link to="/reservation" class="btn btn-primary">Prenota un tavolo</router-link>
            <router-link to="/menu" class="btn-link">Esplora il menu →</router-link>
          </div>
          <div class="hero-stats">
            <div class="stat">
              <span class="stat-num">35<em>+</em></span>
              <span class="stat-label">Anni di storia</span>
            </div>
            <div class="stat">
              <span class="stat-num">40<em>+</em></span>
              <span class="stat-label">Specialità in carta</span>
            </div>
            <div class="stat">
              <span class="stat-num">7</span>
              <span class="stat-label">Giorni su 7*</span>
            </div>
          </div>
        </div>

        <div class="hero-visual reveal" style="transition-delay: 0.15s">
          <img :src="interiorImg" alt="Interno del Bar Gemini" class="hero-img" />
          <div class="floating-card">
            <span class="fc-label">Vieni a trovarci</span>
            <strong>{{ site.address.short }}</strong>
          </div>
          <div class="hero-badge">
            <span class="badge-est">EST.</span>
            <span class="badge-year">1990</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Experience -->
    <section class="experience">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">L'esperienza</span>
          <h2>Tre buoni motivi per <span class="accent">fermarsi</span>.</h2>
        </div>
        <div class="feature-grid">
          <router-link
            v-for="(f, i) in features"
            :key="f.title"
            to="/menu"
            class="feature-card reveal"
            :style="{ transitionDelay: 0.1 * i + 's' }"
          >
            <div class="feature-img">
              <img :src="f.img" :alt="f.title" />
            </div>
            <h3>{{ f.title }}</h3>
            <p>{{ f.text }}</p>
            <span class="feature-link">Scopri →</span>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Services -->
    <section class="services">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Servizi</span>
          <h2>Oltre <span class="accent">il bar</span>.</h2>
        </div>
        <div class="service-grid">
          <div
            v-for="(s, i) in services"
            :key="s.title"
            class="service-item reveal"
            :style="{ transitionDelay: 0.08 * i + 's' }"
          >
            <span class="service-icon">{{ s.icon }}</span>
            <h4>{{ s.title }}</h4>
            <p>{{ s.text }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Map -->
    <section class="location">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Trovaci</span>
          <h2>Nel cuore di <span class="accent">Reggio Emilia</span>.</h2>
        </div>
        <div class="map-wrap reveal">
          <iframe
            v-if="cookieAccepted"
            title="Mappa Bar Gemini"
            :src="site.mapEmbedUrl"
            width="100%" height="460" style="border:0" allowfullscreen loading="lazy"
            referrerpolicy="no-referrer-when-downgrade"></iframe>
          <div v-else class="map-consent">
            <p>La mappa di Google richiede cookie di terze parti.</p>
            <button class="btn btn-primary" @click="acceptCookies">Mostra la mappa</button>
          </div>
          <div class="map-card">
            <span class="eyebrow">Indirizzo</span>
            <h4>{{ site.address.line1 }}</h4>
            <p>{{ site.address.line2 }}</p>
            <a v-if="site.mapsLink" :href="site.mapsLink" target="_blank" rel="noopener" class="btn-link">Apri in Maps →</a>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta">
      <div class="container cta-inner reveal">
        <span class="eyebrow" style="color: var(--gold)">Ti aspettiamo</span>
        <h2>Pronto per l'esperienza <span class="accent-gold">Gemini</span>?</h2>
        <p>Assicurati il tuo tavolo e, se vuoi, ordina in anticipo dalla nostra cucina.</p>
        <router-link to="/reservation" class="btn btn-cta">Prenota il tuo tavolo</router-link>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* ---- Hero ---- */
.hero {
  padding: 160px 0 110px;
}

.hero-grid {
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  gap: 80px;
  align-items: center;
}

.hero-text h1 {
  font-size: clamp(3rem, 6vw, 5.2rem);
  letter-spacing: -0.03em;
  margin: 22px 0 26px;
}

.lead {
  font-size: 1.2rem;
  color: var(--text-soft);
  max-width: 460px;
  margin-bottom: 38px;
}

.hero-actions {
  display: flex;
  align-items: center;
  gap: 28px;
  flex-wrap: wrap;
}

.hero-stats {
  display: flex;
  gap: 44px;
  margin-top: 56px;
  padding-top: 36px;
  border-top: 1px solid var(--border);
}

.stat-num {
  display: block;
  font-family: var(--font-serif);
  font-size: 2.4rem;
  font-weight: 700;
  color: var(--secondary);
  line-height: 1;
}

.stat-num em {
  color: var(--primary);
  font-style: normal;
}

.stat-label {
  font-size: 0.8rem;
  color: var(--text-soft);
  letter-spacing: 0.02em;
}

/* Hero visual */
.hero-visual {
  position: relative;
}

.hero-img {
  width: 100%;
  aspect-ratio: 4 / 5;
  object-fit: cover;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.floating-card {
  position: absolute;
  left: -32px;
  bottom: 40px;
  background: var(--bg-surface);
  padding: 20px 26px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border);
}

.fc-label {
  display: block;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--primary);
  margin-bottom: 4px;
}

.floating-card strong {
  color: var(--secondary);
  font-size: 1rem;
}

.hero-badge {
  position: absolute;
  top: -26px;
  right: -22px;
  width: 96px;
  height: 96px;
  border-radius: 50%;
  background: var(--primary);
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-md);
  transform: rotate(8deg);
}

.badge-est {
  font-size: 0.62rem;
  letter-spacing: 0.2em;
  opacity: 0.85;
}

.badge-year {
  font-family: var(--font-serif);
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1;
}

/* ---- Section heads ---- */
.section-head {
  margin-bottom: 56px;
}

.section-head h2 {
  font-size: clamp(2.2rem, 4vw, 3.2rem);
  margin-top: 14px;
  max-width: 640px;
}

/* ---- Experience ---- */
.experience {
  padding: var(--section) 0;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 34px;
}

.feature-card {
  display: block;
  text-decoration: none;
  color: inherit;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 18px 18px 30px;
  transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.4s ease, border-color 0.4s ease;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-md);
  border-color: transparent;
}

.feature-img {
  aspect-ratio: 4 / 3;
  border-radius: var(--radius-md);
  overflow: hidden;
  margin-bottom: 24px;
}

.feature-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.7s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.feature-card:hover .feature-img img {
  transform: scale(1.06);
}

.feature-card h3 {
  font-size: 1.6rem;
  margin: 0 6px 10px;
}

.feature-card p {
  color: var(--text-soft);
  margin: 0 6px 18px;
}

.feature-link {
  margin-left: 6px;
  font-weight: 700;
  color: var(--primary);
  font-size: 0.9rem;
}

/* ---- Services ---- */
.services {
  padding: var(--section) 0;
  background: var(--bg-soft);
}

.service-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 30px;
}

.service-item {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 34px 28px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.service-item:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-soft);
}

.service-icon {
  font-size: 2rem;
  display: block;
  margin-bottom: 18px;
}

.service-item h4 {
  font-size: 1.2rem;
  margin-bottom: 8px;
}

.service-item p {
  color: var(--text-soft);
  font-size: 0.95rem;
}

/* ---- Location ---- */
.location {
  padding: var(--section) 0;
}

.map-wrap {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border);
}

.map-wrap iframe {
  display: block;
}

.map-consent {
  height: 460px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 18px;
  text-align: center;
  padding: 30px;
  background: var(--bg-soft);
}

.map-consent p {
  color: var(--text-soft);
  max-width: 320px;
}

.map-card {
  position: absolute;
  top: 34px;
  left: 34px;
  background: var(--bg-surface);
  padding: 30px 34px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  max-width: 280px;
}

.map-card h4 {
  font-size: 1.4rem;
  margin: 10px 0 6px;
}

.map-card p {
  color: var(--text-soft);
  margin-bottom: 16px;
}

/* ---- CTA ---- */
.cta {
  padding: 130px 0;
  background: var(--secondary);
  text-align: center;
}

.cta-inner {
  max-width: 720px;
}

.cta h2 {
  color: #fff;
  font-size: clamp(2.4rem, 5vw, 3.6rem);
  margin: 16px 0 18px;
}

.accent-gold {
  color: var(--gold);
  font-style: italic;
}

.cta p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.15rem;
  margin-bottom: 38px;
}

.btn-cta {
  background: #fff;
  color: var(--secondary);
}

.btn-cta:hover {
  background: var(--primary);
  color: #fff;
}

/* ---- Responsive ---- */
@media (max-width: 980px) {
  .hero-grid {
    grid-template-columns: 1fr;
    gap: 70px;
  }

  .feature-grid {
    grid-template-columns: 1fr;
    max-width: 460px;
    margin: 0 auto;
  }

  .service-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 620px) {
  .hero {
    padding: 120px 0 70px;
  }

  /* Keep the floating accents inside the viewport on small screens */
  .floating-card {
    left: 12px;
    bottom: 14px;
    padding: 16px 20px;
  }

  .hero-badge {
    right: 6px;
    top: -10px;
    width: 78px;
    height: 78px;
  }

  .hero-stats {
    gap: 22px;
  }

  .stat-num {
    font-size: 1.9rem;
  }

  .service-grid {
    grid-template-columns: 1fr;
  }

  .map-card {
    position: static;
    max-width: 100%;
    border-radius: 0;
  }
}
</style>
