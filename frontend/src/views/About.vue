<script setup>
import interiorImg from '../assets/interior.png'
import coffeeImg from '../assets/coffee.png'
import { useScrollReveal } from '../composables/useScrollReveal'

useScrollReveal()

const values = [
  { icon: '☕', title: 'Qualità', text: 'Solo ingredienti selezionati e miscele tostate con cura.' },
  { icon: '🤝', title: 'Ospitalità', text: 'Ogni cliente è parte della famiglia, dal mattino alla sera.' },
  { icon: '📍', title: 'Territorio', text: 'Radici profonde nel cuore di Reggio Emilia dal 1990.' },
]
</script>

<template>
  <div class="about-page">
    <!-- Hero -->
    <section class="about-hero">
      <div class="container">
        <span class="eyebrow reveal">La nostra storia</span>
        <h1 class="reveal">Dal 1990, il cuore di <span class="accent">Reggio Emilia</span>.</h1>
        <p class="reveal lead">
          Un piccolo ritrovo locale diventato un punto di riferimento per chi
          cerca qualità e cortesia in ogni momento della giornata.
        </p>
      </div>
    </section>

    <!-- Story -->
    <section class="story">
      <div class="container story-grid">
        <div class="story-text reveal">
          <h2>Una tradizione di <span class="accent">ospitalità</span></h2>
          <p>
            Nato dalla passione per il caffè perfetto e per l'accoglienza
            sincera, il Bar Gemini è cresciuto insieme alla città di Reggio
            Emilia. Quello che era un piccolo ritrovo locale è diventato un punto
            di riferimento per qualità e cortesia.
          </p>
          <p>
            Dall'espresso veloce del mattino al cocktail ricercato della sera,
            per noi ogni cliente è parte della famiglia. Usiamo solo ingredienti
            selezionati e tecniche tramandate con cura nel tempo.
          </p>
          <div class="signature">Mirko &amp; Stefano</div>
        </div>
        <div class="story-media reveal" style="transition-delay: 0.15s">
          <img :src="interiorImg" alt="La sala principale del Bar Gemini" />
          <span class="media-caption">La Sala Principale</span>
        </div>
      </div>
    </section>

    <!-- Values -->
    <section class="values">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Cosa ci guida</span>
          <h2>I nostri <span class="accent">valori</span>.</h2>
        </div>
        <div class="values-grid">
          <div
            v-for="(v, i) in values"
            :key="v.title"
            class="value-card reveal"
            :style="{ transitionDelay: 0.1 * i + 's' }"
          >
            <span class="value-icon">{{ v.icon }}</span>
            <h3>{{ v.title }}</h3>
            <p>{{ v.text }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Banner -->
    <section class="about-banner">
      <img :src="coffeeImg" alt="" class="banner-bg" />
      <div class="banner-overlay"></div>
      <div class="container banner-inner reveal">
        <h2>Ti aspettiamo per un <span class="accent-gold">buon caffè</span>.</h2>
        <router-link to="/reservation" class="btn btn-cta">Prenota un tavolo</router-link>
      </div>
    </section>
  </div>
</template>

<style scoped>
.about-hero {
  padding: 160px 0 70px;
  text-align: center;
}

.about-hero h1 {
  font-size: clamp(2.6rem, 6vw, 4.6rem);
  margin: 18px auto 22px;
  max-width: 900px;
}

.lead {
  font-size: 1.25rem;
  color: var(--text-soft);
  max-width: 640px;
  margin: 0 auto;
}

/* Story */
.story {
  padding: 80px 0 var(--section);
}

.story-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
}

.story-text h2 {
  font-size: clamp(2rem, 4vw, 3rem);
  margin-bottom: 30px;
}

.story-text p {
  color: var(--text-soft);
  font-size: 1.1rem;
  line-height: 1.85;
  margin-bottom: 24px;
}

.signature {
  font-family: var(--font-serif);
  font-style: italic;
  font-size: 2rem;
  color: var(--secondary);
  margin-top: 36px;
}

.story-media {
  position: relative;
}

.story-media img {
  width: 100%;
  aspect-ratio: 4 / 5;
  object-fit: cover;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.media-caption {
  position: absolute;
  bottom: -18px;
  right: -14px;
  background: var(--bg-surface);
  padding: 12px 26px;
  border-radius: var(--radius-pill);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--secondary);
  box-shadow: var(--shadow-soft);
}

/* Values */
.values {
  padding: var(--section) 0;
  background: var(--bg-soft);
}

.section-head {
  text-align: center;
  margin-bottom: 56px;
}

.section-head h2 {
  font-size: clamp(2rem, 4vw, 3rem);
  margin-top: 12px;
}

.values-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.value-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 44px 34px;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.value-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-md);
}

.value-icon {
  font-size: 2.4rem;
  display: block;
  margin-bottom: 18px;
}

.value-card h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.value-card p {
  color: var(--text-soft);
}

/* Banner */
.about-banner {
  position: relative;
  padding: 120px 0;
  text-align: center;
  overflow: hidden;
}

.banner-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.banner-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(rgba(42, 36, 31, 0.78), rgba(42, 36, 31, 0.86));
}

.banner-inner {
  position: relative;
}

.about-banner h2 {
  color: #fff;
  font-size: clamp(2rem, 5vw, 3.4rem);
  margin-bottom: 32px;
}

.accent-gold {
  color: var(--gold);
  font-style: italic;
}

.btn-cta {
  background: #fff;
  color: var(--secondary);
}

.btn-cta:hover {
  background: var(--primary);
  color: #fff;
}

@media (max-width: 900px) {
  .story-grid {
    grid-template-columns: 1fr;
    gap: 60px;
  }

  .values-grid {
    grid-template-columns: 1fr;
    max-width: 420px;
    margin: 0 auto;
  }
}
</style>
