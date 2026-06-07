<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import api from '../api'
import { useRouter } from 'vue-router'

const reservations = ref([])
const menuItems = ref([])
const router = useRouter()
const activeTab = ref('reservations')
const filterStatus = ref('all')

const selectedReservation = ref(null)
const showConfirm = ref(false)
const pendingStatus = ref('')

// Menu management
const showMenuModal = ref(false)
const isEditing = ref(false)
const currentItem = ref({ name: '', description: '', price: 0, category: 'Primi', image_url: '' })

const categories = ['Consigliati dallo Chef', 'Piatto Unico', 'Primi', 'Secondi', 'Contorni', 'Dolci', 'Bevande']

const fetchAdminData = async () => {
  try {
    const [resResp, menuResp] = await Promise.all([
      api.get('/api/admin/reservations'),
      api.get('/api/menu'),
    ])
    reservations.value = resResp.data
    menuItems.value = menuResp.data
    if (selectedReservation.value) {
      selectedReservation.value =
        reservations.value.find((r) => r.id === selectedReservation.value.id) || null
    }
  } catch (err) {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      router.push('/login')
    }
  }
}

const filteredReservations = computed(() =>
  filterStatus.value === 'all'
    ? reservations.value
    : reservations.value.filter((r) => r.status === filterStatus.value)
)

const stats = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  return {
    pending: reservations.value.filter((r) => r.status === 'pending').length,
    today: reservations.value.filter((r) => r.date === today && r.status === 'confirmed').length,
  }
})

const statusLabel = (s) =>
  s === 'pending' ? 'In Attesa' : s === 'confirmed' ? 'Confermata' : 'Annullata'

const confirmAction = (status) => {
  pendingStatus.value = status
  showConfirm.value = true
}

const executeStatusChange = async () => {
  if (!selectedReservation.value) return
  try {
    await api.patch(`/api/admin/reservations/${selectedReservation.value.id}?status=${pendingStatus.value}`)
    showConfirm.value = false
    await fetchAdminData()
  } catch (error) {
    console.error('Error updating status:', error)
    alert('Impossibile aggiornare lo stato. Riprova.')
  }
}

const openAddMenu = () => {
  isEditing.value = false
  currentItem.value = { name: '', description: '', price: 0, category: 'Primi', image_url: '' }
  showMenuModal.value = true
}

const openEditMenu = (item) => {
  isEditing.value = true
  currentItem.value = { ...item }
  showMenuModal.value = true
}

const saveMenuItem = async () => {
  if (!currentItem.value.name || !currentItem.value.description || !currentItem.value.category) {
    alert('Per favore, compila tutti i campi obbligatori (Nome, Categoria e Descrizione).')
    return
  }
  const payload = {
    name: currentItem.value.name,
    description: currentItem.value.description,
    price: Number(currentItem.value.price) || 0,
    category: currentItem.value.category,
    image_url: currentItem.value.image_url || null,
  }
  try {
    if (isEditing.value) {
      await api.put(`/api/admin/menu/${currentItem.value.id}`, payload)
    } else {
      await api.post('/api/admin/menu', payload)
    }
    showMenuModal.value = false
    await fetchAdminData()
  } catch (error) {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      router.push('/login')
      return
    }
    const detail = error.response?.data?.detail
    const msg = Array.isArray(detail) ? detail.map((d) => d.msg).join(', ') : detail || 'errore di connessione'
    alert('Errore nel salvataggio: ' + msg)
  }
}

const deleteMenuItem = async (id) => {
  if (!confirm('Sei sicuro di voler eliminare questo piatto dal menu?')) return
  try {
    await api.delete(`/api/admin/menu/${id}`)
    await fetchAdminData()
  } catch (error) {
    alert("Errore nell'eliminazione.")
  }
}

const logout = () => {
  localStorage.removeItem('token')
  router.push('/')
}

let pollTimer = null
onMounted(() => {
  fetchAdminData()
  pollTimer = setInterval(fetchAdminData, 30000)
})
onUnmounted(() => clearInterval(pollTimer))
</script>

<template>
  <div class="admin">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="brand-box">
        <div class="logo">Gemini <span class="accent">Staff</span></div>
        <p class="staff-tag">Concierge Portal</p>
      </div>

      <nav class="side-nav">
        <button :class="{ active: activeTab === 'reservations' }" @click="activeTab = 'reservations'">
          <span class="icon">📋</span> Prenotazioni
          <span v-if="stats.pending > 0" class="notif">{{ stats.pending }}</span>
        </button>
        <button :class="{ active: activeTab === 'menu' }" @click="activeTab = 'menu'">
          <span class="icon">🍽️</span> Gestione Menu
        </button>
      </nav>

      <div class="sidebar-foot">
        <div class="user">
          <div class="avatar">A</div>
          <span>Admin</span>
        </div>
        <button class="logout" @click="logout">Esci</button>
      </div>
    </aside>

    <!-- Main -->
    <main class="content">
      <header class="content-head">
        <div>
          <h1 v-if="activeTab === 'reservations'">Gestione <span>Prenotazioni</span></h1>
          <h1 v-else>La nostra <span>Carta</span></h1>
          <p>L'arte dell'accoglienza, ogni giorno.</p>
        </div>
        <div class="stats">
          <div class="stat">
            <label>In attesa</label>
            <div class="val">{{ stats.pending }}</div>
          </div>
          <div class="stat">
            <label>Oggi</label>
            <div class="val accent-val">{{ stats.today }}</div>
          </div>
        </div>
      </header>

      <div class="work-area">
        <div class="primary-col">
          <!-- Reservations -->
          <section v-if="activeTab === 'reservations'">
            <div class="bar">
              <h3>Ultime prenotazioni</h3>
              <div class="filters">
                <button :class="{ active: filterStatus === 'all' }" @click="filterStatus = 'all'">Tutte</button>
                <button :class="{ active: filterStatus === 'pending' }" @click="filterStatus = 'pending'">In attesa</button>
                <button :class="{ active: filterStatus === 'confirmed' }" @click="filterStatus = 'confirmed'">Confermate</button>
              </div>
            </div>

            <div class="list">
              <div
                v-for="res in filteredReservations"
                :key="res.id"
                class="res-row"
                :class="{ selected: selectedReservation?.id === res.id }"
                @click="selectedReservation = res"
              >
                <div class="res-client">
                  <strong>{{ res.name }}</strong>
                  <span>{{ res.email }}</span>
                </div>
                <div class="res-when">
                  <span>{{ res.date }}</span>
                  <span>{{ res.time }}</span>
                  <span>{{ res.guests }} ospiti</span>
                </div>
                <span class="pill" :class="res.status">{{ statusLabel(res.status) }}</span>
              </div>
              <div v-if="filteredReservations.length === 0" class="empty">
                <span>📭</span>
                <p>Nessuna prenotazione in questo elenco.</p>
              </div>
            </div>
          </section>

          <!-- Menu -->
          <section v-if="activeTab === 'menu'">
            <div class="bar">
              <h3>{{ menuItems.length }} piatti in carta</h3>
              <button class="btn-add" @click="openAddMenu">+ Aggiungi piatto</button>
            </div>
            <div class="list">
              <div v-for="item in menuItems" :key="item.id" class="menu-row">
                <div class="thumb" v-if="item.image_url"><img :src="item.image_url" :alt="item.name" /></div>
                <div class="thumb placeholder" v-else><span>☕</span></div>
                <div class="menu-info">
                  <strong>{{ item.name }}</strong>
                  <span class="cat">{{ item.category }}</span>
                </div>
                <div class="menu-desc">{{ item.description }}</div>
                <div class="menu-price">€{{ item.price.toFixed(2) }}</div>
                <div class="menu-actions">
                  <button class="btn-edit" @click="openEditMenu(item)">Modifica</button>
                  <button class="btn-del" @click="deleteMenuItem(item.id)">Elimina</button>
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- Detail panel -->
        <aside class="detail" v-if="activeTab === 'reservations'">
          <div v-if="selectedReservation" class="detail-in">
            <span class="pill" :class="selectedReservation.status">{{ statusLabel(selectedReservation.status) }}</span>
            <h2>Dettagli prenotazione</h2>

            <div class="d-section">
              <label>Ospite</label>
              <div class="d-card">
                <h3>{{ selectedReservation.name }}</h3>
                <p>{{ selectedReservation.email }}</p>
                <p>{{ selectedReservation.phone }}</p>
              </div>
            </div>

            <div class="d-section">
              <label>Programmazione</label>
              <div class="d-grid">
                <div><small>Data</small><p>{{ selectedReservation.date }}</p></div>
                <div><small>Ora</small><p>{{ selectedReservation.time }}</p></div>
                <div><small>Ospiti</small><p>{{ selectedReservation.guests }}</p></div>
              </div>
            </div>

            <div class="d-section" v-if="selectedReservation.ordered_items">
              <label>Pre-ordine</label>
              <div class="order">
                <div v-for="item in JSON.parse(selectedReservation.ordered_items)" :key="item.name" class="order-row">
                  <span class="q">{{ item.qty }}×</span>
                  <span>{{ item.name }}</span>
                </div>
              </div>
            </div>

            <div class="d-foot">
              <template v-if="selectedReservation.status === 'pending'">
                <button class="btn-approve" @click="confirmAction('confirmed')">Approva prenotazione</button>
                <button class="btn-reject" @click="confirmAction('cancelled')">Annulla</button>
              </template>
              <template v-else>
                <p class="note">Stato attuale: <strong>{{ statusLabel(selectedReservation.status) }}</strong></p>
                <button class="btn-toggle" @click="confirmAction(selectedReservation.status === 'confirmed' ? 'cancelled' : 'confirmed')">
                  Cambia in {{ selectedReservation.status === 'confirmed' ? 'Annullata' : 'Confermata' }}
                </button>
              </template>
            </div>
          </div>
          <div v-else class="detail-empty">
            <span>👈</span>
            <p>Seleziona una prenotazione per vedere i dettagli e il pre-ordine.</p>
          </div>
        </aside>
      </div>
    </main>

    <!-- Confirm modal -->
    <transition name="fade">
      <div v-if="showConfirm" class="overlay" @click="showConfirm = false">
        <div class="modal" @click.stop>
          <div class="modal-icon">{{ pendingStatus === 'confirmed' ? '✅' : '❌' }}</div>
          <h3>{{ pendingStatus === 'confirmed' ? 'Conferma prenotazione' : 'Annulla prenotazione' }}</h3>
          <p>Segnare questa prenotazione come <strong>{{ statusLabel(pendingStatus) }}</strong>?</p>
          <div class="modal-btns">
            <button class="btn-confirm" :class="pendingStatus" @click="executeStatusChange">
              Sì, {{ pendingStatus === 'confirmed' ? 'approva' : 'annulla' }}
            </button>
            <button class="btn-cancel" @click="showConfirm = false">Indietro</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Menu modal -->
    <transition name="fade">
      <div v-if="showMenuModal" class="overlay" @click="showMenuModal = false">
        <div class="modal modal-wide" @click.stop>
          <h3>{{ isEditing ? 'Modifica piatto' : 'Aggiungi al menu' }}</h3>
          <div class="form-grid">
            <div class="fg">
              <label>Nome del piatto</label>
              <input v-model="currentItem.name" placeholder="Es. Tortelli Verdi" />
            </div>
            <div class="fg">
              <label>Categoria</label>
              <select v-model="currentItem.category">
                <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
              </select>
            </div>
            <div class="fg full">
              <label>Descrizione</label>
              <textarea v-model="currentItem.description" placeholder="Ingredienti e preparazione…"></textarea>
            </div>
            <div class="fg">
              <label>Prezzo (€)</label>
              <input type="number" step="0.5" v-model.number="currentItem.price" />
            </div>
            <div class="fg">
              <label>URL immagine (opzionale)</label>
              <input v-model="currentItem.image_url" placeholder="https://…" />
            </div>
          </div>
          <div class="modal-btns">
            <button class="btn-confirm confirmed" @click="saveMenuItem">Salva</button>
            <button class="btn-cancel" @click="showMenuModal = false">Annulla</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.admin {
  display: flex;
  min-height: 100vh;
  background: var(--bg-white);
  color: var(--text-main);
}

/* ---- Sidebar ---- */
.sidebar {
  width: 264px;
  flex-shrink: 0;
  background: var(--secondary);
  color: rgba(255, 255, 255, 0.7);
  display: flex;
  flex-direction: column;
  padding: 34px 26px;
  position: sticky;
  top: 0;
  height: 100vh;
}

.brand-box {
  margin-bottom: 46px;
}

.logo {
  font-family: var(--font-serif);
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
}

.logo .accent {
  color: var(--gold);
}

.staff-tag {
  font-size: 0.6rem;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.45);
  margin-top: 6px;
}

.side-nav {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.side-nav button {
  display: flex;
  align-items: center;
  gap: 13px;
  width: 100%;
  text-align: left;
  border: none;
  background: none;
  color: rgba(255, 255, 255, 0.7);
  padding: 14px 16px;
  border-radius: var(--radius-sm);
  font-family: var(--font-sans);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.25s ease, color 0.25s ease;
}

.side-nav button:hover {
  background: rgba(255, 255, 255, 0.07);
  color: #fff;
}

.side-nav button.active {
  background: var(--primary);
  color: #fff;
}

.notif {
  margin-left: auto;
  background: var(--gold);
  color: var(--secondary);
  font-size: 0.72rem;
  font-weight: 800;
  padding: 1px 9px;
  border-radius: var(--radius-pill);
}

.sidebar-foot {
  border-top: 1px solid rgba(255, 255, 255, 0.12);
  padding-top: 18px;
}

.user {
  display: flex;
  align-items: center;
  gap: 11px;
  margin-bottom: 14px;
}

.avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: var(--primary);
  color: #fff;
  display: grid;
  place-items: center;
  font-weight: 700;
  font-size: 0.85rem;
}

.user span {
  color: #fff;
  font-weight: 600;
}

.logout {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.55);
  font-weight: 600;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 6px 0;
  transition: color 0.2s ease;
}

.logout:hover {
  color: #fff;
}

/* ---- Content ---- */
.content {
  flex-grow: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.content-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 24px;
  padding: 44px 48px 30px;
  border-bottom: 1px solid var(--border);
}

.content-head h1 {
  font-size: 2.4rem;
}

.content-head h1 span {
  color: var(--primary);
  font-style: italic;
}

.content-head p {
  color: var(--text-soft);
  margin-top: 6px;
}

.stats {
  display: flex;
  gap: 16px;
}

.stat {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 14px 24px;
  text-align: center;
  min-width: 92px;
}

.stat label {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-soft);
}

.val {
  font-family: var(--font-serif);
  font-size: 1.9rem;
  font-weight: 700;
  color: var(--secondary);
}

.accent-val {
  color: var(--primary);
}

.work-area {
  flex-grow: 1;
  display: flex;
  min-height: 0;
}

.primary-col {
  flex-grow: 1;
  min-width: 0;
  padding: 32px 48px;
  overflow-y: auto;
}

.bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.bar h3 {
  font-size: 1.2rem;
}

.filters {
  display: flex;
  gap: 8px;
}

.filters button {
  border: 1px solid var(--border);
  background: var(--bg-surface);
  color: var(--text-soft);
  padding: 8px 16px;
  border-radius: var(--radius-pill);
  font-family: var(--font-sans);
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filters button.active {
  background: var(--secondary);
  color: #fff;
  border-color: var(--secondary);
}

.list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Reservation rows */
.res-row {
  display: flex;
  align-items: center;
  gap: 24px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 20px 24px;
  cursor: pointer;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
}

.res-row:hover {
  border-color: var(--primary);
  transform: translateX(3px);
}

.res-row.selected {
  border-color: var(--primary);
  box-shadow: inset 3px 0 0 var(--primary);
}

.res-client {
  width: 230px;
  flex-shrink: 0;
}

.res-client strong {
  display: block;
  color: var(--secondary);
}

.res-client span {
  font-size: 0.84rem;
  color: var(--text-soft);
}

.res-when {
  display: flex;
  gap: 18px;
  flex-grow: 1;
}

.res-when span {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--secondary);
}

.pill {
  font-size: 0.64rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 6px 13px;
  border-radius: var(--radius-pill);
  white-space: nowrap;
}

.pill.pending {
  background: #fdf3e0;
  color: #b97e15;
}

.pill.confirmed {
  background: #e7f4ec;
  color: #2e7d52;
}

.pill.cancelled {
  background: #fbeaea;
  color: #c0392b;
}

.empty {
  text-align: center;
  padding: 70px 0;
  color: var(--text-soft);
}

.empty span {
  font-size: 2.4rem;
  display: block;
  margin-bottom: 12px;
}

/* Menu rows */
.btn-add {
  background: var(--secondary);
  color: #fff;
  border: none;
  padding: 11px 22px;
  border-radius: var(--radius-pill);
  font-family: var(--font-sans);
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease;
}

.btn-add:hover {
  background: var(--primary);
  transform: translateY(-2px);
}

.menu-row {
  display: grid;
  grid-template-columns: 64px 1fr 2fr auto auto;
  align-items: center;
  gap: 20px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 14px 22px;
}

.thumb {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  border: 1px solid var(--border);
  background: var(--bg-soft);
}

.thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumb.placeholder {
  display: grid;
  place-items: center;
  font-size: 1.6rem;
}

.menu-info strong {
  display: block;
  color: var(--secondary);
}

.menu-info .cat {
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--primary);
}

.menu-desc {
  color: var(--text-soft);
  font-size: 0.9rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.menu-price {
  font-family: var(--font-serif);
  font-weight: 700;
  font-size: 1.2rem;
  color: var(--secondary);
  white-space: nowrap;
}

.menu-actions {
  display: flex;
  gap: 8px;
}

.btn-edit,
.btn-del {
  border: none;
  padding: 9px 15px;
  border-radius: var(--radius-sm);
  font-family: var(--font-sans);
  font-weight: 600;
  font-size: 0.82rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-edit {
  background: var(--bg-soft);
  color: var(--secondary);
}

.btn-edit:hover {
  background: var(--secondary);
  color: #fff;
}

.btn-del {
  background: #fbeaea;
  color: #c0392b;
}

.btn-del:hover {
  background: #c0392b;
  color: #fff;
}

/* ---- Detail panel ---- */
.detail {
  width: 400px;
  flex-shrink: 0;
  background: var(--bg-surface);
  border-left: 1px solid var(--border);
  overflow-y: auto;
}

.detail-in {
  padding: 40px 34px;
}

.detail-in h2 {
  font-size: 1.7rem;
  margin: 14px 0 32px;
}

.d-section {
  margin-bottom: 30px;
}

.d-section label {
  display: block;
  font-size: 0.66rem;
  font-weight: 800;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--text-soft);
  margin-bottom: 12px;
}

.d-card {
  background: var(--bg-soft);
  border-radius: var(--radius-md);
  padding: 22px 24px;
}

.d-card h3 {
  font-size: 1.2rem;
  margin-bottom: 6px;
}

.d-card p {
  color: var(--text-soft);
  font-size: 0.92rem;
}

.d-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.d-grid > div {
  background: var(--bg-soft);
  border-radius: var(--radius-sm);
  padding: 14px 10px;
  text-align: center;
}

.d-grid small {
  display: block;
  font-size: 0.62rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-soft);
  margin-bottom: 5px;
}

.d-grid p {
  font-weight: 700;
  color: var(--secondary);
}

.order {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.order-row {
  display: flex;
  gap: 12px;
  padding: 12px 16px;
  background: var(--bg-soft);
  border-radius: var(--radius-sm);
}

.order-row .q {
  font-weight: 800;
  color: var(--primary);
}

.order-row span:last-child {
  color: var(--secondary);
  font-weight: 600;
}

.d-foot {
  margin-top: 36px;
  padding-top: 26px;
  border-top: 1px dashed var(--border);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.btn-approve {
  background: var(--primary);
  color: #fff;
  border: none;
  padding: 17px;
  border-radius: var(--radius-sm);
  font-family: var(--font-sans);
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s ease;
}

.btn-approve:hover {
  background: var(--primary-dark);
}

.btn-reject {
  background: none;
  border: 1px solid var(--border);
  color: #c0392b;
  padding: 15px;
  border-radius: var(--radius-sm);
  font-family: var(--font-sans);
  font-weight: 700;
  cursor: pointer;
}

.btn-reject:hover {
  border-color: #c0392b;
}

.note {
  text-align: center;
  color: var(--text-soft);
  font-size: 0.9rem;
}

.btn-toggle {
  background: none;
  border: none;
  color: var(--primary);
  font-family: var(--font-sans);
  font-weight: 700;
  cursor: pointer;
  text-decoration: underline;
  text-underline-offset: 3px;
}

.detail-empty {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 60px 40px;
  color: var(--text-soft);
}

.detail-empty span {
  font-size: 2.6rem;
  margin-bottom: 18px;
}

/* ---- Modals ---- */
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(28, 20, 12, 0.55);
  backdrop-filter: blur(6px);
  display: grid;
  place-items: center;
  padding: 24px;
  z-index: 1000;
}

.modal {
  background: var(--bg-surface);
  padding: 44px;
  border-radius: var(--radius-lg);
  max-width: 430px;
  width: 100%;
  text-align: center;
  box-shadow: var(--shadow-hover);
}

.modal-wide {
  max-width: 580px;
  text-align: left;
}

.modal-icon {
  font-size: 2.6rem;
  margin-bottom: 16px;
}

.modal h3 {
  font-size: 1.6rem;
  margin-bottom: 12px;
}

.modal > p {
  color: var(--text-soft);
  margin-bottom: 28px;
}

.modal-btns {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 26px;
}

.btn-confirm {
  border: none;
  padding: 16px;
  border-radius: var(--radius-sm);
  font-family: var(--font-sans);
  font-weight: 700;
  color: #fff;
  cursor: pointer;
}

.btn-confirm.confirmed {
  background: var(--secondary);
}

.btn-confirm.cancelled {
  background: #c0392b;
}

.btn-cancel {
  background: var(--bg-soft);
  border: none;
  padding: 16px;
  border-radius: var(--radius-sm);
  font-family: var(--font-sans);
  font-weight: 700;
  color: var(--secondary);
  cursor: pointer;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin: 26px 0 4px;
}

.fg.full {
  grid-column: span 2;
}

.fg label {
  display: block;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-soft);
  margin-bottom: 8px;
}

.fg input,
.fg select,
.fg textarea {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-family: var(--font-sans);
  font-size: 0.95rem;
  background: var(--bg-white);
  color: var(--text-main);
}

.fg input:focus,
.fg select:focus,
.fg textarea:focus {
  outline: none;
  border-color: var(--primary);
}

.fg textarea {
  height: 96px;
  resize: none;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ---- Responsive ---- */
@media (max-width: 1100px) {
  .work-area {
    flex-direction: column;
  }

  .detail {
    width: auto;
    border-left: none;
    border-top: 1px solid var(--border);
  }
}

@media (max-width: 760px) {
  .admin {
    flex-direction: column;
  }

  .sidebar {
    width: auto;
    height: auto;
    position: static;
    flex-direction: row;
    align-items: center;
    padding: 16px 20px;
    gap: 16px;
  }

  .brand-box {
    margin-bottom: 0;
  }

  .staff-tag {
    display: none;
  }

  .side-nav {
    flex-direction: row;
    flex-grow: 1;
    justify-content: center;
  }

  .side-nav button {
    width: auto;
  }

  .sidebar-foot {
    border-top: none;
    padding-top: 0;
  }

  .user {
    display: none;
  }

  .content-head {
    flex-direction: column;
    align-items: flex-start;
    padding: 28px 24px 22px;
  }

  .primary-col {
    padding: 24px;
  }

  .res-row {
    flex-wrap: wrap;
    gap: 12px;
  }

  .res-client {
    width: 100%;
  }

  .menu-row {
    grid-template-columns: 56px 1fr auto;
  }

  .menu-desc {
    display: none;
  }

  .menu-actions {
    grid-column: 2 / 4;
    justify-content: flex-end;
  }
}
</style>
