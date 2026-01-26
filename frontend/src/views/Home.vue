<script setup>
import interiorImg from '../assets/interior.png'
import coffeeImg from '../assets/coffee.png'
import pastriesImg from '../assets/pastries.png'
import aperitivoImg from '../assets/aperitivo_mock.png'
</script>

<template>
  <div class="home-v3">
    <!-- Hero -->
    <section class="hero-v2">
      <div class="container hero-grid">
        <div class="hero-text fade-up">
          <span class="pre-title">DAL 1990 IN REGGIO EMILIA</span>
          <h1>Elegance in <br/> Every <span class="highlight">Detail</span>.</h1>
          <p>Join us for the perfect blend of Italian tradition and contemporary atmosphere.</p>
          <div class="hero-buttons">
            <router-link to="/reservation" class="btn-solid">Book Table</router-link>
            <router-link to="/menu" class="btn-outline">The Menu</router-link>
          </div>
        </div>
        <div class="hero-image-container fade-up" style="animation-delay: 0.2s">
          <img :src="interiorImg" alt="Bar Gemini Interior" class="main-hero-img" />
          <div class="hero-blob"></div>
        </div>
      </div>
    </section>

    <!-- Experience Sections -->
    <section class="experience-strip">
      <div class="container grid-3">
        <router-link to="/menu" class="feature-card fade-up">
          <div class="feature-img-box">
            <img :src="coffeeImg" alt="Coffee" />
          </div>
          <h3>Crafted Coffee</h3>
          <p>The perfect start to your day, roasted and prepared with passion.</p>
        </router-link>
        
        <router-link to="/menu" class="feature-card fade-up" style="animation-delay: 0.1s">
          <div class="feature-img-box">
            <img :src="pastriesImg" alt="Pastries" />
          </div>
          <h3>Modern Bakery</h3>
          <p>Daily handmade delicacies that melt in your mouth.</p>
        </router-link>

        <router-link to="/menu" class="feature-card fade-up" style="animation-delay: 0.2s">
          <div class="feature-img-box">
            <img :src="aperitivoImg" alt="Aperitivo" />
          </div>
          <h3>Curated Spirits</h3>
          <p>The Italian ritual, served with hand-picked snacks and cocktails.</p>
        </router-link>
      </div>
    </section>

    <!-- Call to action -->
    <section class="cta-banner fade-up">
      <div class="container cta-inner">
        <h2>Ready for the <span>Gemini Experience</span>?</h2>
        <router-link to="/reservation" class="btn-solid">Reserve Your Table</router-link>
      </div>
    </section>
  </div>
</template>

<style scoped>
.hero-v2 {
  padding: 100px 0 60px;
}

.hero-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 80px;
}

.pre-title {
  display: block;
  font-size: 0.8rem;
  letter-spacing: 3px;
  color: var(--text-soft);
  margin-bottom: 20px;
}

h1 {
  font-size: 5rem;
  line-height: 1.1;
  letter-spacing: -3px;
  margin-bottom: 30px;
}

.highlight {
  color: var(--primary);
}

.hero-text p {
  font-size: 1.25rem;
  color: var(--text-soft);
  margin-bottom: 40px;
  max-width: 500px;
}

.hero-buttons {
  display: flex;
  gap: 20px;
}

.btn-solid {
  background: var(--text-main);
  color: #fff;
  padding: 18px 40px;
  text-decoration: none;
  font-weight: 700;
  border-radius: var(--radius-sm);
  display: inline-block;
}

.btn-outline {
  border: 2px solid var(--text-main);
  padding: 16px 40px;
  text-decoration: none;
  color: var(--text-main);
  font-weight: 700;
  border-radius: var(--radius-sm);
  display: inline-block;
}

.hero-image-container {
  position: relative;
}

.main-hero-img {
  width: 100%;
  border-radius: var(--radius-lg);
  position: relative;
  z-index: 2;
}

.hero-blob {
  position: absolute;
  top: -10%; right: -10%;
  width: 120%; height: 120%;
  background: #f0f0f0;
  border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%;
  z-index: 1;
}

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
}

.feature-card h3 {
  margin: 20px 0 10px;
  font-size: 1.5rem;
}

.feature-img-box {
  width: 100%;
  aspect-ratio: 4/5;
  overflow: hidden;
  border-radius: var(--radius-lg);
}

.feature-img-box img {
  width: 100%; height: 100%;
  object-fit: cover;
  transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.feature-card:hover .feature-img-box img {
  transform: scale(1.1);
}

.cta-banner {
  padding: 150px 0;
  background: var(--bg-soft);
  text-align: center;
}

.cta-banner h2 {
  font-size: 3rem;
  margin-bottom: 40px;
}

.cta-banner span {
  color: var(--primary);
}

@media (max-width: 1024px) {
  h1 { font-size: 3.5rem; }
  .hero-grid, .grid-3 { grid-template-columns: 1fr; }
}
</style>
