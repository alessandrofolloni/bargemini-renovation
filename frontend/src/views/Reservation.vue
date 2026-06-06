<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api'
import interiorImg from '../assets/interior.png'

const step = ref(1)
const menu = ref([])
const loadingMenu = ref(true)

const reservation = ref({
  name: '',
  email: '',
  phone: '',
  date: '',
  time: '',
  guests: 2
})

const selectedItems = ref({}) // { itemId: quantity }

onMounted(async () => {
  // Fetch menu for pre-ordering
  try {
    const response = await api.get('/api/menu')
    menu.value = response.data
  } catch (err) {
    console.error('Could not fetch menu:', err)
    menu.value = []
  } finally {
    loadingMenu.value = false
  }

  // Scroll Animation Logic
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

const updateQty = (id, delta) => {
  const current = selectedItems.value[id] || 0
  const next = Math.max(0, current + delta)
  if (next === 0) {
    delete selectedItems.value[id]
  } else {
    selectedItems.value[id] = next
  }
}

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
      // Fallback for any unknown categories
      if (!categories['Altro']) categories['Altro'] = []
      categories['Altro'].push(item)
    }
  })
  
  return categories
})

const orderedCategoryNames = ['Consigliati dallo Chef', 'Piatto Unico', 'Primi', 'Secondi', 'Contorni', 'Dolci', 'Bevande', 'Altro']

const totalItems = computed(() => {
  return Object.values(selectedItems.value).reduce((a, b) => a + b, 0)
})

const submitReservation = async () => {
  try {
    // Format ordered items as a string for simplicity in DB
    const preOrder = menu.value
      .filter(item => selectedItems.value[item.id])
      .map(item => ({ name: item.name, qty: selectedItems.value[item.id] }))
    
    // Ensure guests is an int
    const payload = {
      ...reservation.value,
      guests: parseInt(reservation.value.guests),
      ordered_items: preOrder.length > 0 ? JSON.stringify(preOrder) : null
    }

    await api.post('/api/reservations', payload)
    
    // Success feedback
    alert('Perfetto! La tua prenotazione e il pre-ordine sono stati confermati.')
    
    // Reset form
    step.value = 1
    reservation.value = { 
      name: '', 
      email: '', 
      phone: '', 
      date: '', 
      time: '', 
      guests: 2 
    }
    selectedItems.value = {}
  } catch (error) {
    console.error(error)
    alert('Qualcosa è andato storto. Controlla i dettagli e riprova.')
  }
}
</script>

<template>
  <div class="page-container">
    <section class="booking-hero">
      <div class="container hero-split">
        <div class="hero-left scroll-reveal">
          <div class="subtitle-badge">CONCIERGE & SAPORI</div>
          <h1>Momenti <span>Perfetti</span>.</h1>
          <p>Assicurati un tavolo e ordina in anticipo dalla nostra cucina per garantirti un'accoglienza impeccabile e deliziosa.</p>
          
          <div class="steps-indicator">
            <div :class="['step-dot', { active: step >= 1 }]"><span>1</span> Dettagli</div>
            <div class="step-line"></div>
            <div :class="['step-dot', { active: step >= 2 }]"><span>2</span> Menu</div>
          </div>

          <div class="contact-details">
            <div class="contact-item">
              <strong>Indirizzo</strong>
              <p>Via Aristotele, 102, Reggio Emilia</p>
            </div>
            <div class="contact-item">
              <strong>Prenotazioni</strong>
              <p>+39 0522 123456</p>
            </div>
          </div>
        </div>
        
        <div class="hero-right scroll-reveal" style="transition-delay: 0.2s">
          <div class="booking-form-card">
            <div class="card-inner">
              <div v-if="step === 1" class="step-content">
                <h2>Il Tuo Invito</h2>
                <form @submit.prevent="step = 2" class="modern-form">
                  <div class="input-group">
                    <label>Nome</label>
                    <input v-model="reservation.name" type="text" placeholder="Nome Completo" required />
                  </div>
                  <div class="input-group">
                    <label>Contatto</label>
                    <input v-model="reservation.email" type="email" placeholder="Indirizzo Email" required />
                  </div>
                  <div class="form-row">
                    <div class="input-group">
                      <label>Telefono</label>
                      <input v-model="reservation.phone" type="tel" placeholder="+39..." required />
                    </div>
                    <div class="input-group">
                      <label>Persone</label>
                      <input v-model.number="reservation.guests" type="number" placeholder="2" required min="1" />
                    </div>
                  </div>
                  <div class="form-row">
                    <div class="input-group">
                      <label>Data</label>
                      <input v-model="reservation.date" type="date" required />
                    </div>
                    <div class="input-group">
                      <label>Orario</label>
                      <input v-model="reservation.time" type="time" required />
                    </div>
                  </div>
                  <button type="submit" class="btn-submit">Continua al Menu</button>
                </form>
              </div>

              <div v-if="step === 2" class="step-content animate-slide">
                <div class="step-header">
                  <button @click="step = 1" class="btn-back">← Indietro</button>
                  <h2>Selezione Gusti</h2>
                </div>
                <p class="step-desc">Seleziona i piatti per riceverli al tuo arrivo.</p>
                
                <div class="quick-menu-list">
                  <div v-if="loadingMenu" class="menu-loader">Caricamento cucina...</div>
                  
                  <template v-for="catName in orderedCategoryNames" :key="catName">
                    <div v-if="menuCategories[catName] && menuCategories[catName].length > 0" class="menu-category-block">
                      <h3 class="category-title">{{ catName }}</h3>
                      
                      <div v-for="item in menuCategories[catName]" :key="item.id" class="mini-item-card">
                        <div class="mini-info">
                          <h4>{{ item.name }}</h4>
                          <span class="mini-price">€{{ item.price.toFixed(2) }}</span>
                        </div>
                        <div class="qty-selector">
                          <button @click="updateQty(item.id, -1)" type="button">-</button>
                          <span class="qty">{{ selectedItems[item.id] || 0 }}</span>
                          <button @click="updateQty(item.id, 1)" type="button">+</button>
                        </div>
                      </div>
                    </div>
                  </template>

                </div>

                <div class="pre-order-footer">
                  <div class="summary">
                    <span>Piatti Selezionati: <strong>{{ totalItems }}</strong></span>
                  </div>
                  <button @click="submitReservation" class="btn-submit">Completa Prenotazione</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <div class="decoration-img scroll-reveal">
      <img :src="interiorImg" alt="" />
    </div>
  </div>
</template>

<style scoped>
.page-container {
  padding-top: 150px;
}

.booking-hero {
  padding-bottom: 100px;
}

.hero-split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 100px;
  align-items: center;
}

.subtitle-badge {
  font-size: 0.7rem;
  letter-spacing: 3px;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 20px;
  text-transform: uppercase;
  border-left: 2px solid var(--primary);
  padding-left: 15px;
}

h1 {
  font-size: 5rem;
  letter-spacing: -3px;
  line-height: 1;
  margin-bottom: 30px;
}

h1 span {
  color: var(--primary);
  font-style: italic;
}

.hero-left p {
  font-size: 1.25rem;
  color: var(--text-soft);
  margin-bottom: 50px;
  max-width: 450px;
  line-height: 1.6;
}

/* Steps Indicator */
.steps-indicator {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 60px;
}

.step-dot {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.8rem;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--text-soft);
  transition: all 0.4s;
}

.step-dot span {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-soft);
  border: 1px solid var(--border);
  border-radius: 50%;
  font-size: 0.7rem;
}

.step-dot.active {
  color: var(--secondary);
}

.step-dot.active span {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary);
}

.step-line {
  flex-grow: 1;
  max-width: 60px;
  height: 1px;
  background: var(--border);
}

.contact-details {
  display: grid;
  gap: 30px;
  border-top: 1px solid var(--border);
  padding-top: 40px;
}

.contact-item strong {
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 2px;
  color: var(--secondary);
  display: block;
  margin-bottom: 5px;
}

.contact-item p {
  margin: 0;
  font-size: 1.1rem;
  color: var(--text-main);
  font-weight: 600;
}

.booking-form-card {
  background: #fff;
  padding: 60px;
  border-radius: var(--radius-lg);
  box-shadow: 0 40px 100px rgba(0,0,0,0.08);
  border: 1px solid var(--border);
  position: relative;
  min-height: 650px;
}

.card-inner {
  position: relative;
  z-index: 2;
}

.booking-form-card::before {
  content: '';
  position: absolute;
  top: 10px; left: 10px; right: 10px; bottom: 10px;
  border: 1px solid var(--border);
  border-radius: 12px;
  pointer-events: none;
}

.booking-form-card h2 {
  margin-bottom: 40px;
  font-size: 2.2rem;
  text-align: center;
  font-family: var(--font-serif);
  color: var(--secondary);
}

.modern-form {
  display: grid;
  gap: 20px;
}

/* Step 2 Specifics */
.step-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 10px;
}

.btn-back {
  background: none;
  border: none;
  font-weight: 700;
  color: var(--primary);
  cursor: pointer;
  padding: 0;
}

.step-desc {
  font-size: 0.95rem;
  color: var(--text-soft);
  margin-bottom: 30px;
  text-align: center;
}

.quick-menu-list {
  max-height: 380px;
  overflow-y: auto;
  padding-right: 15px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* Custom Scrollbar */
.quick-menu-list::-webkit-scrollbar {
  width: 4px;
}
.quick-menu-list::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 4px;
}

.mini-item-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: var(--bg-soft);
  border-radius: 12px;
  border: 1px solid transparent;
  transition: all 0.3s;
}

.mini-item-card:hover {
  border-color: var(--border);
  background: #fff;
}

.mini-cat {
  font-size: 0.6rem;
  text-transform: uppercase;
  color: var(--primary);
  font-weight: 800;
  display: block;
  margin-bottom: 4px;
}

.mini-info h4 {
  font-size: 1.1rem;
  margin-bottom: 4px;
  color: var(--secondary);
}

.mini-price {
  font-family: var(--font-serif);
  font-weight: 700;
  color: var(--text-main);
  font-size: 0.9rem;
}

.qty-selector {
  display: flex;
  align-items: center;
  gap: 15px;
  background: #fff;
  padding: 5px;
  border-radius: 50px;
  border: 1px solid var(--border);
}

.qty-selector button {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: var(--bg-soft);
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.qty-selector button:hover {
  background: var(--primary);
  color: #fff;
}

.qty {
  font-family: var(--font-serif);
  font-weight: 700;
  min-width: 20px;
  text-align: center;
}

.pre-order-footer {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid var(--border);
}

.summary {
  text-align: center;
  font-size: 0.9rem;
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.input-group label {
  display: block;
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--secondary);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

input {
  width: 100%;
  padding: 16px 0;
  border: none;
  border-bottom: 1px solid var(--border);
  font-size: 1.1rem;
  box-sizing: border-box;
  background: transparent;
  font-family: var(--font-serif);
  color: var(--text-main);
  transition: border-color 0.3s;
}

input:focus {
  outline: none;
  border-color: var(--primary);
}

.btn-submit {
  width: 100%;
  background: var(--text-main);
  color: #fff;
  padding: 22px;
  border: none;
  border-radius: 4px;
  font-weight: 700;
  font-size: 1rem;
  margin-top: 10px;
  cursor: pointer;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: background 0.3s;
}

.btn-submit:hover {
  background: var(--primary);
}

.decoration-img {
  width: 100%;
  height: 500px;
  overflow: hidden;
  margin-top: 50px;
}

.decoration-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 1.5s ease;
}

.scroll-reveal {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 1s ease, transform 1s ease;
}

.scroll-reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

.scroll-reveal.visible img {
  transform: scale(1.05);
}

.animate-slide {
  animation: slideIn 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
}

@keyframes slideIn {
  from { opacity: 0; transform: translateX(20px); }
  to { opacity: 1; transform: translateX(0); }
}

@media (max-width: 968px) {
  .hero-split { grid-template-columns: 1fr; gap: 60px; }
  .booking-form-card { padding: 40px; }
  h1 { font-size: 3.5rem; }
}

/* Menu Categories */
.menu-category-block {
  margin-bottom: 30px;
}

.category-title {
  font-family: var(--font-serif);
  font-size: 1.2rem;
  color: var(--secondary);
  border-bottom: 1px solid var(--border);
  padding-bottom: 10px;
  margin-bottom: 15px;
  font-weight: 700;
}
</style>
