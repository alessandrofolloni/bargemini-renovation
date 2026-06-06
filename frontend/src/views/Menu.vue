<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api'

const menu = ref([])
const loading = ref(true)

const menuCategories = computed(() => {
  if (!menu.value.length) return {}
  
  const categories = {
    'Consigliati dallo Chef': [],
    'Piatto Unico': [],
    'Primi': [],
    'Secondi': [],
    'Contorni': [],
    'Dolci': [],
    'Bevande': []
  }

  menu.value.forEach(item => {
    // Mapping categorie da Inglese (DB) a Italiano (UI)
    const catMap = {
      'Suggested by Chef': 'Consigliati dallo Chef',
      'Single Dish': 'Piatto Unico',
      'First': 'Primi',
      'Second': 'Secondi',
      'Sides': 'Contorni',
      'Desserts': 'Dolci',
      'Drinks': 'Bevande'
    }
    const category = catMap[item.category] || item.category

    if (categories[category]) {
      categories[category].push(item)
    } else {
      if (!categories['Altro']) categories['Altro'] = []
      categories['Altro'].push(item)
    }
  })
  
  return categories
})

const orderedCategoryNames = ['Consigliati dallo Chef', 'Piatto Unico', 'Primi', 'Secondi', 'Contorni', 'Dolci', 'Bevande', 'Altro']

onMounted(async () => {
  try {
    const response = await api.get('/api/menu')
    menu.value = response.data
  } catch (error) {
    console.error('API Connection Failed:', error)
    menu.value = [] // Clear items if fetch fails so we don't show old mock data
  } finally {
    loading.value = false
    
    // Initialize Observer after DOM update
    setTimeout(() => {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) entry.target.classList.add('visible')
        })
      }, { threshold: 0.1, rootMargin: "0px 0px -50px 0px" })

      document.querySelectorAll('.scroll-reveal').forEach((el) => observer.observe(el))
    }, 100)
  }
})
</script>

<template>
  <div class="page-container">
    <div class="container section-header scroll-reveal">
      <h1>Il <span>Menu</span>.</h1>
      <p v-if="menu.length > 0">La nostra selezione curata di {{ menu.length }} specialità italiane.</p>
      <p v-else>Una selezione curata di eccellenza italiana, dalla nostra cucina alla vostra tavola.</p>
    </div>

    <section class="menu-display">
      <div class="container">
        <div v-if="loading" class="loader">Caricamento menu...</div>
        <div v-else class="menu-sections-wrapper">
          
          <template v-for="catName in orderedCategoryNames" :key="catName">
            <div v-if="menuCategories[catName] && menuCategories[catName].length > 0" class="category-section scroll-reveal">
              <div class="category-header">
                <h2>{{ catName }}</h2>
                <div class="header-line"></div>
              </div>

              <div class="menu-grid-modern">
                <div v-for="(item, index) in menuCategories[catName]" :key="item.id" class="menu-item-card">
                  <div class="card-image-wrapper" v-if="item.image_url">
                    <img :src="item.image_url" :alt="item.name" class="item-visual" />
                    <div class="item-overlay"></div>
                  </div>
                  <div class="card-content">
                    <div class="item-top">
                      <span class="category-tag">{{ item.category }}</span>
                      <span class="price">€{{ item.price.toFixed(2) }}</span>
                    </div>
                    <h3>{{ item.name }}</h3>
                    <p>{{ item.description }}</p>
                  </div>
                </div>
              </div>
            </div>
          </template>

        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.page-container {
  padding-top: 180px;
}

.section-header {
  padding-bottom: 80px;
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

.section-header p {
  font-size: 1.25rem;
  color: var(--text-soft);
  max-width: 600px;
  margin: 0 auto;
}

/* Category Sections */
.category-section {
  margin-bottom: 80px;
}

.category-header {
  display: flex;
  align-items: center;
  gap: 30px;
  margin-bottom: 40px;
}

.category-header h2 {
  font-family: var(--font-serif);
  font-size: 2.5rem;
  color: var(--secondary);
  white-space: nowrap;
}

.header-line {
  height: 1px;
  background: var(--border);
  flex-grow: 1;
}

.menu-sections-wrapper {
  padding-bottom: 100px;
}

.menu-display {
  padding: 80px 0;
  background: var(--bg-soft);
  min-height: 600px;
  border-top: 1px solid var(--border);
}

.menu-grid-modern {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 40px;
}

.menu-item-card {
  background: var(--glass);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-lg);
  border: 1px solid var(--glass-border);
  transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-soft);
}

.menu-item-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: var(--shadow-hover);
  border-color: var(--primary);
}

.card-image-wrapper {
  position: relative;
  height: 250px;
  overflow: hidden;
}

.item-visual {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.menu-item-card:hover .item-visual {
  transform: scale(1.05);
}

.item-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, transparent 60%, rgba(0,0,0,0.05));
}

.card-content {
  padding: 40px;
  flex-grow: 1;
}

.item-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid var(--border);
  padding-bottom: 15px;
}

.category-tag {
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--primary);
  letter-spacing: 2px;
}

.price {
  font-family: var(--font-serif);
  font-weight: 700;
  font-size: 1.4rem;
  color: var(--text-main);
}

.menu-item-card h3 {
  font-size: 1.8rem;
  margin-bottom: 15px;
  color: var(--secondary);
}

.menu-item-card p {
  color: var(--text-soft);
  line-height: 1.6;
  font-size: 1rem;
}

/* Animations */
.scroll-reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.scroll-reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

@media (max-width: 768px) {
  h1 { font-size: 3.5rem; }
  .menu-grid-modern { grid-template-columns: 1fr; }
  .menu-item-card { padding: 30px; }
  .category-header h2 { font-size: 1.8rem; }
}
</style>
