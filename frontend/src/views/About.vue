<script setup>
import { onMounted } from 'vue'
import interiorImg from '../assets/interior.png'

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
  <div class="page-container">
    <section class="about-hero">
      <div class="container scroll-reveal">
        <h1>La Nostra <span>Storia</span>.</h1>
        <p class="lead">Bar Gemini è il cuore pulsante di Reggio Emilia dal 1990.</p>
      </div>
    </section>

    <section class="story-content">
      <div class="container content-grid">
        <div class="text-block scroll-reveal">
          <h2>Una Tradizione di <span class="highlight">Ospitalità</span></h2>
          <p>
            Nato dalla passione per il caffè perfetto e per l'accoglienza sincera, 
            il Bar Gemini è cresciuto insieme alla città di Reggio Emilia. 
            Quello che era nato come un piccolo ritrovo locale è diventato oggi un punto di riferimento 
            per chi cerca qualità e cortesia in ogni momento della giornata.
          </p>
          <p>
            Dall'espresso veloce del mattino al cocktail ricercato della sera, 
            per noi ogni cliente è parte della famiglia. Utilizziamo solo ingredienti 
            selezionati e seguiamo tecniche tramandate con cura nel tempo.
          </p>
          <div class="signature">Mirko & Stefano</div>
        </div>
        <div class="image-block scroll-reveal" style="transition-delay: 0.2s">
          <img :src="interiorImg" alt="Our Interior" />
          <div class="img-caption">La Sala Principale, circa 2024</div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.page-container {
  padding-top: 180px;
}

.about-hero {
  padding-bottom: 80px;
  border-bottom: 1px solid var(--border);
  text-align: center;
}

h1 {
  font-size: 5rem;
  letter-spacing: -3px;
  margin-bottom: 20px;
}

h1 span {
  color: var(--primary);
  font-style: italic;
}

.lead {
  font-size: 1.4rem;
  color: var(--text-soft);
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.5;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 100px;
  padding: 120px 0;
  align-items: center;
}

.text-block h2 {
  font-size: 3rem;
  margin-bottom: 40px;
  line-height: 1.1;
}

.highlight {
  color: var(--primary);
  font-family: var(--font-serif);
  font-style: italic;
}

.text-block p {
  font-size: 1.1rem;
  color: var(--text-soft);
  margin-bottom: 30px;
  line-height: 1.8;
}

.signature {
  font-family: 'Playfair Display', serif;
  font-size: 2rem;
  color: var(--secondary);
  margin-top: 40px;
  font-style: italic;
}

.image-block {
  position: relative;
}

.image-block img {
  width: 100%;
  border-radius: 20px;
  box-shadow: 0 40px 80px rgba(0,0,0,0.1);
}

.img-caption {
  position: absolute;
  bottom: -30px;
  right: -20px;
  background: white;
  padding: 15px 30px;
  border-radius: 50px;
  font-weight: 700;
  font-size: 0.8rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  color: var(--secondary);
}

/* Animations */
.scroll-reveal {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 1s ease, transform 1s ease;
}

.scroll-reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

@media (max-width: 968px) {
  .content-grid { grid-template-columns: 1fr; gap: 60px; }
  h1 { font-size: 3.5rem; }
  .page-container { padding-top: 150px; }
}
</style>
