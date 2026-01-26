<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const menu = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/menu')
    menu.value = response.data
  } catch (error) {
    menu.value = [
      { id: 1, name: "Espresso Artigianale", description: "Our signature blend espresso.", price: 1.50, category: "Bar" },
      { id: 2, name: "Cornetto al Pistacchio", description: "Freshly baked handmade pastry.", price: 2.00, category: "Bakery" },
      { id: 3, name: "Negroni Sbagliato", description: "A local favorite for more than 30 years.", price: 8.00, category: "Drinks" }
    ]
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="page-container">
    <div class="container section-header">
      <h1>The <span>Menu</span>.</h1>
      <p>A curated selection of Italian excellence.</p>
    </div>

    <section class="menu-display">
      <div class="container">
        <div v-if="loading" class="loader">Loading menu...</div>
        <div v-else class="menu-grid-modern">
          <div v-for="item in menu" :key="item.id" class="menu-item-card fade-up">
            <div class="item-top">
              <span class="category-tag">{{ item.category }}</span>
              <span class="price">€{{ item.price.toFixed(2) }}</span>
            </div>
            <h3>{{ item.name }}</h3>
            <p>{{ item.description }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.page-container {
  padding-top: 150px;
}

.section-header {
  padding-bottom: 60px;
}

h1 {
  font-size: 5rem;
  letter-spacing: -3px;
}

h1 span {
  color: var(--primary);
}

.section-header p {
  font-size: 1.25rem;
  color: var(--text-soft);
  margin-top: 20px;
}

.menu-display {
  padding: 80px 0;
  background: var(--bg-soft);
  min-height: 500px;
}

.menu-grid-modern {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 30px;
}

.menu-item-card {
  background: #fff;
  padding: 40px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  transition: all 0.4s ease;
}

.menu-item-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.05);
  border-color: var(--primary);
}

.item-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.category-tag {
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--primary);
  letter-spacing: 2px;
}

.price {
  font-weight: 700;
  font-size: 1.1rem;
}

.menu-item-card h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.menu-item-card p {
  color: var(--text-soft);
  line-height: 1.5;
}

@media (max-width: 768px) {
  h1 { font-size: 3.5rem; }
  .menu-grid-modern { grid-template-columns: 1fr; }
}
</style>
