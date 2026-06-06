<script setup>
import { onMounted, ref } from 'vue'
import interiorImg from '../assets/interior.png'
import coffeeImg from '../assets/coffee.png'
import pastriesImg from '../assets/pastries.png'
import aperitivoImg from '../assets/aperitivo_mock.png'
import logoImg from '../assets/logo_original.jpg'

// Scroll Animation Logic
onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible')
      }
    })
  }, { threshold: 0.1, rootMargin: "0px 0px -50px 0px" })

  document.querySelectorAll('.scroll-reveal').forEach((el) => {
    observer.observe(el)
  })
})
</script>

<template>
  <div class="home-v3">
    <!-- Hero v3 -->
    <section class="hero-v2">
      <div class="container hero-grid">
        <div class="hero-text scroll-reveal">
          <div class="hero-brand-card">
            <img :src="logoImg" alt="Bar Gemini" class="hero-logo-img" />
            <span class="hero-est">EST. 1990</span>
          </div>
          <h1>L'Eccellenza dell'<span>Aperitivo</span>.</h1>
          <p class="lead">Lo storico ritrovo di Reggio Emilia, dove la passione per il caffè incontra l'arte del buon bere.</p>
          <div class="hero-buttons">
            <router-link to="/reservation" class="btn-solid-premium">Prenota un Tavolo</router-link>
            <router-link to="/menu" class="btn-text-link">Esplora il Menu →</router-link>
          </div>
        </div>
        <div class="hero-main-visual scroll-reveal" style="transition-delay: 0.2s">
          <div class="image-stack">
            <img :src="interiorImg" alt="Bar Gemini Interior" class="stack-base" />
            <div class="floating-accent-card animate-float">
              <strong>Vieni a trovarci</strong>
              <p>Via Aristotele 102, RE</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Experience Sections -->
    <section class="experience-strip">
      <div class="container grid-3">
        <router-link to="/menu" class="feature-card scroll-reveal">
          <div class="feature-img-box">
            <img :src="coffeeImg" alt="Coffee" />
          </div>
          <div class="feature-content">
            <h3>Caffè d'Autore</h3>
            <p>Il modo perfetto per iniziare la giornata, tostato e preparato con passione.</p>
          </div>
        </router-link>
        
        <router-link to="/menu" class="feature-card scroll-reveal" style="transition-delay: 0.1s">
          <div class="feature-img-box">
            <img :src="pastriesImg" alt="Pastries" />
          </div>
          <div class="feature-content">
            <h3>Pasticceria Moderna</h3>
            <p>Delizie artigianali quotidiane che si sciolgono in bocca.</p>
          </div>
        </router-link>

        <router-link to="/menu" class="feature-card scroll-reveal" style="transition-delay: 0.2s">
          <div class="feature-img-box">
            <img :src="aperitivoImg" alt="Aperitivo" />
          </div>
          <div class="feature-content">
            <h3>Drink & Cocktail</h3>
            <p>Il rito dell'aperitivo italiano, servito con una selezione dei migliori spiriti e stuzzichini.</p>
          </div>
        </router-link>
      </div>
    </section>

    <!-- Services Section -->
    <section class="services-section">
      <div class="container">
        <div class="section-header scroll-reveal">
          <div class="section-label">SERVIZI</div>
          <h2>Oltre <span>il Bar</span>.</h2>
        </div>
        <div class="services-grid">
          <div class="service-item scroll-reveal">
            <span class="icon">🎟️</span>
            <h4>Ticket Restaurant</h4>
            <p>Accettiamo i principali buoni pasto per la tua pausa pranzo.</p>
          </div>
          <div class="service-item scroll-reveal" style="transition-delay: 0.1s">
            <span class="icon">🚬</span>
            <h4>Tabacchi</h4>
            <p>Servizio tabaccheria e articoli per fumatori disponibili all'interno.</p>
          </div>
          <div class="service-item scroll-reveal" style="transition-delay: 0.2s">
            <span class="icon">🏧</span>
            <h4>Servizio ATM</h4>
            <p>Comodo prelievo contanti senza lasciare il comfort del bar.</p>
          </div>
          <div class="service-item scroll-reveal" style="transition-delay: 0.3s">
            <span class="icon">🎰</span>
            <h4>Lotto & Giochi</h4>
            <p>Tenta la fortuna con Lotto, Superenalotto e Gratta e Vinci.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Map Section -->
    <section class="location-map scroll-reveal">
      <div class="container">
        <div class="section-header">
          <div class="section-label">TROVACI</div>
          <h2>Ci trovi nel cuore di <span>Reggio Emilia</span>.</h2>
        </div>
        <div class="map-wrapper">
          <iframe 
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2830.826315254134!2d10.630018312061218!3d44.69255627095493!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x477fef6ea1a9e623%3A0xc0688a531d279774!2sVia%20Aristotele%2C%20102%2C%2042122%20Reggio%20Emilia%20RE!5e0!3m2!1sit!2sit!4v1706466000000!5m2!1sit!2sit" 
            width="100%" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade">
          </iframe>
          <div class="map-overlay-info">
            <h4>Via Aristotele 102</h4>
            <p>42122 Reggio Emilia (RE)</p>
            <a href="https://maps.app.goo.gl/..." target="_blank" class="btn-text-link">Apri in Maps →</a>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to action -->
    <section class="cta-banner scroll-reveal">
      <div class="container cta-inner">
        <h2>Pronto per l'<span>Esperienza Gemini</span>?</h2>
        <router-link to="/reservation" class="btn-solid-premium">Prenota il Tuo Tavolo</router-link>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* Hero Styles */
.hero-v2 {
  padding: 180px 0 100px;
}

.hero-grid {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  align-items: center;
  gap: 100px;
}

.hero-brand-card {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.hero-logo-img {
  height: 80px;
  width: auto;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

.hero-est {
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 4px;
  color: var(--primary);
  border-left: 2px solid #eee;
  padding-left: 20px;
}

h1 {
  font-size: 5.5rem;
  line-height: 0.95;
  letter-spacing: -4px;
  margin-bottom: 30px;
}

h1 span,
.highlight {
  color: var(--primary);
  font-style: italic;
}

.hero-text p {
  font-size: 1.25rem;
  color: #555;
  margin-bottom: 40px;
  max-width: 550px;
  line-height: 1.6;
}

.hero-buttons {
  display: flex;
  align-items: center;
  gap: 30px;
}

.btn-solid-premium {
  background: var(--text-main);
  color: #fff;
  padding: 22px 45px;
  text-decoration: none;
  font-weight: 800;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.15);
  transition: all 0.3s;
}

.btn-solid-premium:hover { transform: translateY(-3px); box-shadow: 0 15px 40px rgba(0,0,0,0.2); }

.btn-text-link {
  text-decoration: none;
  color: var(--text-main);
  font-weight: 800;
  font-size: 1rem;
  transition: opacity 0.3s;
}

/* Visual Stack */
.hero-main-visual { position: relative; }
.image-stack { position: relative; }

.stack-base {
  width: 100%;
  border-radius: 30px;
  box-shadow: 0 50px 100px rgba(0,0,0,0.1);
}

.floating-accent-card {
  position: absolute;
  bottom: 40px;
  left: -40px;
  background: var(--glass);
  backdrop-filter: blur(20px);
  padding: 30px 40px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--glass-border);
  z-index: 10;
}

.floating-accent-card strong { display: block; font-size: 1.2rem; margin-bottom: 5px; color: var(--secondary); }
.floating-accent-card p { margin: 0; color: var(--text-soft); font-size: 0.95rem; font-weight: 500; }

/* Animations */
.scroll-reveal {
  opacity: 0;
  transform: translateY(40px);
  transition: all 1s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.scroll-reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Experience Strip */
.experience-strip {
  padding: 120px 0;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}

.feature-card {
  text-decoration: none;
  color: inherit;
  display: block;
}

.feature-img-box {
  width: 100%;
  aspect-ratio: 4/5;
  overflow: hidden;
  border-radius: 12px;
  margin-bottom: 20px;
  position: relative;
}

.feature-img-box img {
  width: 100%; height: 100%;
  object-fit: cover;
  transition: transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.feature-card:hover .feature-img-box img {
  transform: scale(1.05);
}

.feature-content h3 {
  font-size: 1.8rem;
  margin-bottom: 10px;
  color: var(--secondary);
}

.feature-content p {
  color: var(--text-soft);
  font-size: 1rem;
  line-height: 1.6;
}

/* Services / Amenities */
.services-section {
  padding: 120px 0;
  border-top: 1px solid var(--border);
  background: white;
}

.section-label {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 3px;
  color: var(--primary);
  margin-bottom: 15px;
  text-transform: uppercase;
}

.section-header h2 {
  font-size: 3.5rem;
  margin-bottom: 60px;
  max-width: 600px;
}

.section-header span {
  font-style: italic;
  font-family: var(--font-serif);
  color: var(--secondary);
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 40px;
  border-top: 1px solid var(--border);
}

.service-item {
  padding-top: 40px;
  border-right: 1px solid var(--border);
  padding-right: 30px;
}

.service-item:last-child {
  border-right: none;
}

.icon {
  font-size: 2.5rem;
  display: block;
  margin-bottom: 20px;
  filter: grayscale(100%);
  transition: transform 0.3s;
}

.service-item:hover .icon {
  transform: translateY(-5px);
  filter: grayscale(0%);
}

.service-item h4 {
  font-size: 1.25rem;
  margin-bottom: 10px;
  color: var(--secondary);
}

@media (max-width: 1024px) {
  h1 { font-size: 3.5rem; }
  .grid-3 { grid-template-columns: 1fr; gap: 60px; }
  .services-grid { grid-template-columns: 1fr 1fr; border-top: none; }
  .service-item { border-right: none; border-top: 1px solid var(--border); }
}

/* Map Section Styles */
.location-map {
  padding: 120px 0;
  background: var(--bg-soft);
}

.map-wrapper {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border);
}

.map-overlay-info {
  position: absolute;
  top: 40px;
  right: 40px;
  background: var(--glass);
  backdrop-filter: blur(20px);
  padding: 40px;
  border-radius: var(--radius-md);
  border: 1px solid var(--glass-border);
  box-shadow: var(--shadow-md);
  max-width: 300px;
}

.map-overlay-info h4 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.map-overlay-info p {
  color: var(--text-soft);
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .map-overlay-info {
    position: relative;
    top: 0; right: 0;
    max-width: 100%;
    border-radius: 0;
    border: none;
    border-top: 1px solid var(--border);
  }
}

/* CTA Banner Styles */
.cta-banner {
  padding: 180px 0;
  background: white;
  text-align: center;
  border-top: 1px solid var(--border);
}

.cta-inner h2 {
  font-size: 4rem;
  margin-bottom: 50px;
  line-height: 1;
}

.cta-inner span {
  color: var(--primary);
  font-style: italic;
}
</style>
