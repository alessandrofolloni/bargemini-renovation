<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api'
import { useScrollReveal } from '../composables/useScrollReveal'

const menu = ref([])
const loading = ref(true)
const activeCat = ref('')
const { refresh } = useScrollReveal()

const CAT_ORDER = ['Consigliati dallo Chef', 'Piatto Unico', 'Primi', 'Secondi', 'Contorni', 'Dolci', 'Bevande', 'Altro']

// Legacy English → Italian labels (older rows may still use English categories)
const CAT_MAP = {
  'Suggested by Chef': 'Consigliati dallo Chef',
  'Single Dish': 'Piatto Unico',
  First: 'Primi',
  Second: 'Secondi',
  Sides: 'Contorni',
  Desserts: 'Dolci',
  Drinks: 'Bevande',
}

const grouped = computed(() => {
  const out = {}
  for (const item of menu.value) {
    const cat = CAT_MAP[item.category] || item.category || 'Altro'
    ;(out[cat] ||= []).push(item)
  }
  return out
})

const sections = computed(() =>
  CAT_ORDER.filter((c) => grouped.value[c]?.length).map((c) => ({ name: c, items: grouped.value[c] }))
)

const scrollTo = (name) => {
  document.getElementById('cat-' + name)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

onMounted(async () => {
  try {
    const { data } = await api.get('/api/menu')
    menu.value = data
    if (sections.value.length) activeCat.value = sections.value[0].name
  } catch (e) {
    console.error('API Connection Failed:', e)
    menu.value = []
  } finally {
    loading.value = false
    refresh()
  }
})
</script>

<template>
  <div class="menu-page">
    <header class="menu-hero">
      <div class="container">
        <span class="eyebrow reveal">La nostra carta</span>
        <h1 class="reveal">Il <span class="accent">Menu</span>.</h1>
        <p class="reveal">
          {{ menu.length ? `Una selezione curata di ${menu.length} specialità italiane, dalla nostra cucina alla vostra tavola.` : 'Eccellenza italiana, dalla nostra cucina alla vostra tavola.' }}
        </p>
      </div>
    </header>

    <!-- Sticky category chips -->
    <nav v-if="sections.length" class="cat-nav">
      <div class="container cat-nav-inner">
        <button
          v-for="s in sections"
          :key="s.name"
          class="cat-chip"
          @click="scrollTo(s.name)"
        >{{ s.name }}</button>
      </div>
    </nav>

    <section class="menu-body">
      <div class="container">
        <div v-if="loading" class="state">Caricamento del menu…</div>
        <div v-else-if="!menu.length" class="state">
          Menu momentaneamente non disponibile. Riprova tra poco.
        </div>

        <div
          v-for="s in sections"
          :key="s.name"
          :id="'cat-' + s.name"
          class="cat-section reveal"
        >
          <div class="cat-head">
            <h2>{{ s.name }}</h2>
            <span class="cat-count">{{ s.items.length }} piatti</span>
          </div>

          <ul class="dish-list">
            <li v-for="item in s.items" :key="item.id" class="dish">
              <div v-if="item.image_url" class="dish-thumb">
                <img :src="item.image_url" :alt="item.name" />
              </div>
              <div class="dish-main">
                <div class="dish-top">
                  <h3>{{ item.name }}</h3>
                  <span class="leader"></span>
                  <span class="dish-price">€{{ item.price.toFixed(2) }}</span>
                </div>
                <p v-if="item.description" class="dish-desc">{{ item.description }}</p>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </section>

    <div class="menu-cta">
      <div class="container">
        <h2>Vuoi assaggiare di persona?</h2>
        <router-link to="/reservation" class="btn btn-primary">Prenota un tavolo</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.menu-hero {
  padding: 150px 0 50px;
  text-align: center;
}

.menu-hero h1 {
  font-size: clamp(3rem, 7vw, 5rem);
  margin: 16px 0 18px;
}

.menu-hero p {
  color: var(--text-soft);
  font-size: 1.2rem;
  max-width: 560px;
  margin: 0 auto;
}

/* Sticky chips */
.cat-nav {
  position: sticky;
  top: 72px;
  z-index: 500;
  background: rgba(246, 241, 234, 0.85);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}

.cat-nav-inner {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding-top: 16px;
  padding-bottom: 16px;
  scrollbar-width: none;
}

.cat-nav-inner::-webkit-scrollbar {
  display: none;
}

.cat-chip {
  flex: 0 0 auto;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  padding: 9px 20px;
  font-family: var(--font-sans);
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--secondary);
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.25s ease;
}

.cat-chip:hover {
  background: var(--secondary);
  color: #fff;
  border-color: var(--secondary);
}

/* Body */
.menu-body {
  padding: 80px 0 100px;
}

.state {
  text-align: center;
  color: var(--text-soft);
  padding: 80px 0;
  font-size: 1.1rem;
}

.cat-section {
  max-width: 880px;
  margin: 0 auto 80px;
  scroll-margin-top: 150px;
}

.cat-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 34px;
  padding-bottom: 16px;
  border-bottom: 2px solid var(--secondary);
}

.cat-head h2 {
  font-size: 2.1rem;
}

.cat-count {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--primary);
  white-space: nowrap;
}

.dish-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 28px;
}

.dish {
  display: flex;
  gap: 22px;
  align-items: flex-start;
}

.dish-thumb {
  flex: 0 0 84px;
  width: 84px;
  height: 84px;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--border);
}

.dish-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.dish-main {
  flex: 1;
  min-width: 0;
}

.dish-top {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.dish-top h3 {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--secondary);
  white-space: normal;
}

.leader {
  flex: 1;
  height: 0;
  border-bottom: 1.5px dotted var(--border);
  transform: translateY(-4px);
  min-width: 24px;
}

.dish-price {
  font-family: var(--font-serif);
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--primary);
  white-space: nowrap;
}

.dish-desc {
  color: var(--text-soft);
  font-size: 0.98rem;
  line-height: 1.6;
  margin-top: 6px;
  max-width: 620px;
}

/* CTA */
.menu-cta {
  background: var(--bg-soft);
  border-top: 1px solid var(--border);
  padding: 90px 0;
  text-align: center;
}

.menu-cta h2 {
  font-size: clamp(1.8rem, 4vw, 2.6rem);
  margin-bottom: 28px;
}

@media (max-width: 620px) {
  .menu-hero {
    padding-top: 120px;
  }

  .dish-top {
    flex-wrap: wrap;
  }

  .leader {
    display: none;
  }

  .dish-price {
    margin-left: auto;
  }
}
</style>
