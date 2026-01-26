<script setup>
import interiorImg from '../assets/interior.png'
</script>

<template>
  <div class="page-container">
    <section class="about-hero">
      <div class="container">
        <h1>Our <span>Story</span>.</h1>
        <p class="lead">Bar Gemini has been the heartbeat of Reggio Emilia since 1990.</p>
      </div>
    </section>

    <section class="story-content">
      <div class="container content-grid">
        <div class="text-block">
          <h2>A Tradition of Quality</h2>
          <p>
            Founded with a passion for the perfect espresso and the Italian art of hospitality, 
            Bar Gemini has evolved from a local favorite into a modern landmark. 
            We believe that every cup of coffee and every plate we serve should tell a story 
            of craftsmanship and dedication.
          </p>
          <p>
            Whether it's your first morning espresso or a late-evening Negroni, 
            you are part of our family. Our ingredients are sourced locally, 
            and our techniques are passed down through generations.
          </p>
        </div>
        <div class="image-block">
          <img :src="interiorImg" alt="Our Interior" />
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.page-container {
  padding-top: 150px;
}

.about-hero {
  padding-bottom: 80px;
  border-bottom: 1px solid var(--border);
}

h1 {
  font-size: 5rem;
  letter-spacing: -3px;
}

h1 span {
  color: var(--primary);
}

.lead {
  font-size: 1.5rem;
  color: var(--text-soft);
  margin-top: 20px;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  padding: 100px 0;
  align-items: center;
}

.text-block h2 {
  font-size: 2.5rem;
  margin-bottom: 30px;
}

.text-block p {
  font-size: 1.1rem;
  color: var(--text-soft);
  margin-bottom: 20px;
}

.image-block img {
  width: 100%;
  border-radius: var(--radius-lg);
  box-shadow: 0 40px 80px rgba(0,0,0,0.1);
}

@media (max-width: 968px) {
  .content-grid { grid-template-columns: 1fr; gap: 40px; }
  h1 { font-size: 3.5rem; }
}
</style>
