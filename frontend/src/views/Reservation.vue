<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api'
import { useScrollReveal } from '../composables/useScrollReveal'

const step = ref(1)
const menu = ref([])
const loadingMenu = ref(true)
const submitting = ref(false)
const done = ref(false)

useScrollReveal()

const reservation = ref({ name: '', email: '', phone: '', date: '', time: '', guests: 2 })
const selectedItems = ref({}) // { itemId: quantity }

const CAT_ORDER = ['Consigliati dallo Chef', 'Piatto Unico', 'Primi', 'Secondi', 'Contorni', 'Dolci', 'Bevande', 'Altro']
const CAT_MAP = {
  'Suggested by Chef': 'Consigliati dallo Chef',
  'Single Dish': 'Piatto Unico',
  First: 'Primi',
  Second: 'Secondi',
  Sides: 'Contorni',
  Desserts: 'Dolci',
  Drinks: 'Bevande',
}

const today = new Date().toISOString().split('T')[0]

onMounted(async () => {
  try {
    const { data } = await api.get('/api/menu')
    menu.value = data
  } catch (e) {
    console.error('Could not fetch menu:', e)
    menu.value = []
  } finally {
    loadingMenu.value = false
  }
})

const updateQty = (id, delta) => {
  const next = Math.max(0, (selectedItems.value[id] || 0) + delta)
  if (next === 0) delete selectedItems.value[id]
  else selectedItems.value[id] = next
}

const sections = computed(() => {
  const out = {}
  for (const item of menu.value) {
    const cat = CAT_MAP[item.category] || item.category || 'Altro'
    ;(out[cat] ||= []).push(item)
  }
  return CAT_ORDER.filter((c) => out[c]?.length).map((c) => ({ name: c, items: out[c] }))
})

const totalItems = computed(() => Object.values(selectedItems.value).reduce((a, b) => a + b, 0))

const totalPrice = computed(() =>
  menu.value.reduce((sum, i) => sum + (selectedItems.value[i.id] || 0) * i.price, 0)
)

const submitReservation = async () => {
  submitting.value = true
  try {
    const preOrder = menu.value
      .filter((i) => selectedItems.value[i.id])
      .map((i) => ({ name: i.name, qty: selectedItems.value[i.id] }))

    await api.post('/api/reservations', {
      ...reservation.value,
      guests: parseInt(reservation.value.guests),
      ordered_items: preOrder.length ? JSON.stringify(preOrder) : null,
    })
    done.value = true
  } catch (e) {
    console.error(e)
    alert('Qualcosa è andato storto. Controlla i dettagli e riprova.')
  } finally {
    submitting.value = false
  }
}

const reset = () => {
  done.value = false
  step.value = 1
  reservation.value = { name: '', email: '', phone: '', date: '', time: '', guests: 2 }
  selectedItems.value = {}
}
</script>

<template>
  <div class="reservation-page">
    <div class="container res-grid">
      <!-- Left: pitch -->
      <aside class="res-intro reveal">
        <span class="eyebrow">Concierge & Sapori</span>
        <h1>Momenti <span class="accent">perfetti</span>.</h1>
        <p>
          Assicurati un tavolo e ordina in anticipo dalla nostra cucina per
          un'accoglienza impeccabile e deliziosa.
        </p>

        <div class="res-info">
          <div class="info-row">
            <span class="info-label">Indirizzo</span>
            <span class="info-val">Via Aristotele 102, Reggio Emilia</span>
          </div>
          <div class="info-row">
            <span class="info-label">Prenotazioni</span>
            <span class="info-val">+39 0522 123456</span>
          </div>
          <div class="info-row">
            <span class="info-label">Orari</span>
            <span class="info-val">Lun–Sab · 07:00 – 24:00</span>
          </div>
        </div>
      </aside>

      <!-- Right: booking card -->
      <div class="res-card reveal" style="transition-delay: 0.12s">
        <!-- Success -->
        <div v-if="done" class="res-done">
          <div class="done-check">✓</div>
          <h2>Prenotazione confermata!</h2>
          <p>
            Grazie {{ reservation.name || '' }}, abbiamo ricevuto la tua
            richiesta. Ti aspettiamo al Bar Gemini.
          </p>
          <button class="btn btn-primary" @click="reset">Nuova prenotazione</button>
        </div>

        <template v-else>
          <!-- Steps -->
          <div class="steps">
            <div class="step" :class="{ active: step >= 1, current: step === 1 }">
              <span class="step-n">1</span> Dettagli
            </div>
            <span class="step-bar"></span>
            <div class="step" :class="{ active: step >= 2, current: step === 2 }">
              <span class="step-n">2</span> Pre-ordine
            </div>
          </div>

          <!-- Step 1 -->
          <form v-if="step === 1" class="res-form" @submit.prevent="step = 2">
            <h2>I tuoi dettagli</h2>
            <div class="field">
              <label>Nome completo</label>
              <input v-model="reservation.name" type="text" placeholder="Mario Rossi" required />
            </div>
            <div class="field">
              <label>Email</label>
              <input v-model="reservation.email" type="email" placeholder="mario@email.it" required />
            </div>
            <div class="field-row">
              <div class="field">
                <label>Telefono</label>
                <input v-model="reservation.phone" type="tel" placeholder="+39 …" required />
              </div>
              <div class="field">
                <label>Persone</label>
                <input v-model.number="reservation.guests" type="number" min="1" max="30" required />
              </div>
            </div>
            <div class="field-row">
              <div class="field">
                <label>Data</label>
                <input v-model="reservation.date" type="date" :min="today" required />
              </div>
              <div class="field">
                <label>Orario</label>
                <input v-model="reservation.time" type="time" required />
              </div>
            </div>
            <button type="submit" class="btn btn-primary full">Continua al pre-ordine →</button>
            <button type="button" class="skip-link" @click="submitReservation" :disabled="submitting">
              {{ submitting ? 'Invio…' : 'Prenota senza pre-ordine' }}
            </button>
          </form>

          <!-- Step 2 -->
          <div v-else class="res-preorder">
            <div class="preorder-head">
              <button class="back" @click="step = 1">← Indietro</button>
              <h2>Pre-ordine</h2>
              <p>Seleziona i piatti da trovare pronti al tuo arrivo (facoltativo).</p>
            </div>

            <div class="dish-scroll">
              <div v-if="loadingMenu" class="state">Caricamento cucina…</div>
              <div v-for="s in sections" :key="s.name" class="po-cat">
                <h4>{{ s.name }}</h4>
                <div v-for="item in s.items" :key="item.id" class="po-row">
                  <div class="po-info">
                    <span class="po-name">{{ item.name }}</span>
                    <span class="po-price">€{{ item.price.toFixed(2) }}</span>
                  </div>
                  <div class="qty">
                    <button type="button" @click="updateQty(item.id, -1)" :disabled="!selectedItems[item.id]">−</button>
                    <span>{{ selectedItems[item.id] || 0 }}</span>
                    <button type="button" @click="updateQty(item.id, 1)">+</button>
                  </div>
                </div>
              </div>
            </div>

            <div class="preorder-foot">
              <div class="po-summary">
                <span>{{ totalItems }} piatti</span>
                <strong v-if="totalPrice">€{{ totalPrice.toFixed(2) }}</strong>
              </div>
              <button class="btn btn-primary full" @click="submitReservation" :disabled="submitting">
                {{ submitting ? 'Invio…' : 'Completa prenotazione' }}
              </button>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
.reservation-page {
  padding: 150px 0 var(--section);
}

.res-grid {
  display: grid;
  grid-template-columns: 0.9fr 1.1fr;
  gap: 70px;
  align-items: start;
}

/* Intro */
.res-intro {
  position: sticky;
  top: 110px;
}

.res-intro h1 {
  font-size: clamp(2.6rem, 5vw, 4rem);
  margin: 18px 0 22px;
}

.res-intro > p {
  color: var(--text-soft);
  font-size: 1.15rem;
  max-width: 420px;
  margin-bottom: 44px;
}

.res-info {
  display: grid;
  gap: 22px;
  border-top: 1px solid var(--border);
  padding-top: 36px;
}

.info-label {
  display: block;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--primary);
  margin-bottom: 5px;
}

.info-val {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--secondary);
}

/* Card */
.res-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: 46px;
  min-height: 560px;
}

.res-card h2 {
  font-size: 1.9rem;
  margin-bottom: 28px;
}

/* Steps */
.steps {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 38px;
}

.step {
  display: flex;
  align-items: center;
  gap: 9px;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-soft);
}

.step-n {
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background: var(--bg-soft);
  border: 1px solid var(--border);
  font-size: 0.78rem;
}

.step.active {
  color: var(--secondary);
}

.step.active .step-n {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary);
}

.step-bar {
  flex: 1;
  height: 1px;
  background: var(--border);
  max-width: 60px;
}

/* Form */
.res-form {
  display: grid;
  gap: 22px;
}

.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.field label {
  display: block;
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--secondary);
  margin-bottom: 9px;
}

.field input {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--bg-white);
  font-family: var(--font-sans);
  font-size: 1rem;
  color: var(--text-main);
  transition: border-color 0.25s ease, box-shadow 0.25s ease;
}

.field input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(181, 58, 43, 0.12);
}

.full {
  width: 100%;
  margin-top: 6px;
}

.skip-link {
  background: none;
  border: none;
  color: var(--text-soft);
  font-family: var(--font-sans);
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  text-underline-offset: 3px;
}

.skip-link:hover {
  color: var(--primary);
}

.skip-link:disabled {
  opacity: 0.5;
  cursor: default;
}

/* Pre-order */
.preorder-head h2 {
  margin-bottom: 6px;
}

.preorder-head > p {
  color: var(--text-soft);
  font-size: 0.95rem;
  margin-bottom: 20px;
}

.back {
  background: none;
  border: none;
  color: var(--primary);
  font-weight: 700;
  cursor: pointer;
  padding: 0;
  margin-bottom: 12px;
  font-family: var(--font-sans);
}

.dish-scroll {
  max-height: 360px;
  overflow-y: auto;
  padding-right: 10px;
  margin: 0 -6px;
  padding-left: 6px;
}

.state {
  color: var(--text-soft);
  text-align: center;
  padding: 30px 0;
}

.po-cat h4 {
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--primary);
  margin: 22px 0 10px;
}

.po-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}

.po-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.po-name {
  font-weight: 600;
  color: var(--secondary);
}

.po-price {
  font-size: 0.85rem;
  color: var(--text-soft);
}

.qty {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 0 0 auto;
}

.qty button {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 1px solid var(--border);
  background: var(--bg-surface);
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  color: var(--secondary);
  transition: all 0.2s ease;
}

.qty button:hover:not(:disabled) {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary);
}

.qty button:disabled {
  opacity: 0.4;
  cursor: default;
}

.qty span {
  min-width: 18px;
  text-align: center;
  font-weight: 700;
  font-family: var(--font-serif);
}

.preorder-foot {
  margin-top: 26px;
  padding-top: 22px;
  border-top: 1px solid var(--border);
}

.po-summary {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 16px;
  font-weight: 600;
  color: var(--text-soft);
}

.po-summary strong {
  font-family: var(--font-serif);
  font-size: 1.3rem;
  color: var(--primary);
}

/* Success */
.res-done {
  text-align: center;
  padding: 30px 10px;
}

.done-check {
  width: 76px;
  height: 76px;
  margin: 0 auto 26px;
  border-radius: 50%;
  background: #e8f3ec;
  color: #2e7d52;
  display: grid;
  place-items: center;
  font-size: 2.2rem;
}

.res-done h2 {
  margin-bottom: 14px;
}

.res-done p {
  color: var(--text-soft);
  max-width: 360px;
  margin: 0 auto 32px;
}

@media (max-width: 900px) {
  .res-grid {
    grid-template-columns: 1fr;
    gap: 50px;
  }

  .res-intro {
    position: static;
  }
}

@media (max-width: 560px) {
  .res-card {
    padding: 30px 24px;
  }

  .field-row {
    grid-template-columns: 1fr;
  }
}
</style>
