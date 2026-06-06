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

// Menu Management
const showMenuModal = ref(false)
const isEditing = ref(false)
const currentItem = ref({
  name: '',
  description: '',
  price: 0,
  category: 'Primi',
  image_url: ''
})

const categories = ['Consigliati dallo Chef', 'Piatto Unico', 'Primi', 'Secondi', 'Contorni', 'Dolci', 'Bevande']

const fetchAdminData = async () => {
  try {
    const [resResp, menuResp] = await Promise.all([
      api.get('/api/admin/reservations'),
      api.get('/api/menu')
    ])
    reservations.value = resResp.data
    menuItems.value = menuResp.data
    
    if (selectedReservation.value) {
      selectedReservation.value = reservations.value.find(r => r.id === selectedReservation.value.id) || null
    }
  } catch (err) {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      router.push('/login')
    }
  }
}

const filteredReservations = computed(() => {
  if (filterStatus.value === 'all') return reservations.value
  return reservations.value.filter(r => r.status === filterStatus.value)
})

const stats = computed(() => {
  return {
    pending: reservations.value.filter(r => r.status === 'pending').length,
    today: reservations.value.filter(r => {
      const today = new Date().toISOString().split('T')[0]
      return r.date === today && r.status === 'confirmed'
    }).length
  }
})

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
    image_url: currentItem.value.image_url || null
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
    console.error('Save error:', error.response?.data || error.message)
    const detail = error.response?.data?.detail
    const msg = Array.isArray(detail) ? detail.map(d => d.msg).join(', ') : (detail || 'errore di connessione')
    alert('Errore nel salvataggio: ' + msg)
  }
}

const deleteMenuItem = async (id) => {
  if (!confirm('Sei sicuro di voler eliminare questo piatto dal patrimonio?')) return

  try {
    await api.delete(`/api/admin/menu/${id}`)
    await fetchAdminData()
  } catch (error) {
    alert('Errore nell\'eliminazione.')
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

onUnmounted(() => {
  clearInterval(pollTimer)
})
</script>

<template>
  <div class="admin-dashboard">
    <aside class="sidebar">
      <div class="brand-box">
        <div class="logo">GEMINI <span class="accent">STAFF</span></div>
        <p class="staff-tag">CONCIERGE PORTAL</p>
      </div>
      
      <nav class="side-nav">
        <button :class="{active: activeTab === 'reservations'}" @click="activeTab = 'reservations'">
          <span class="icon">📜</span> Prenotazioni
          <span v-if="stats.pending > 0" class="notif-badge">{{ stats.pending }}</span>
        </button>
        <button :class="{active: activeTab === 'menu'}" @click="activeTab = 'menu'">
          <span class="icon">🍽️</span> Gestione Menu
        </button>
      </nav>

      <div class="sidebar-footer">
        <div class="user-pill">
          <div class="avatar">A</div>
          <span>Admin</span>
        </div>
        <button @click="logout" class="btn-logout">Esci</button>
      </div>
    </aside>

    <main class="admin-main">
      <header class="admin-header">
        <div class="header-left">
          <h1>Gestione <span>Prenotazioni</span></h1>
          <p>L'arte dell'accoglienza, ogni giorno.</p>
        </div>
        <div class="quick-stats">
          <div class="stat-card">
            <label>In Attesa</label>
            <div class="val">{{ stats.pending }}</div>
          </div>
          <div class="stat-card">
            <label>Oggi</label>
            <div class="val highlight">{{ stats.today }}</div>
          </div>
        </div>
      </header>

      <div class="admin-grid">
        <div class="main-content-area">
          <section v-if="activeTab === 'reservations'" class="dash-content">
            <div class="content-actions">
              <h3>Ultime Prenotazioni</h3>
              <div class="filters">
                <button :class="{active: filterStatus === 'all'}" @click="filterStatus = 'all'">Tutte</button>
                <button :class="{active: filterStatus === 'pending'}" @click="filterStatus = 'pending'">In Attesa</button>
                <button :class="{active: filterStatus === 'confirmed'}" @click="filterStatus = 'confirmed'">Confermate</button>
              </div>
            </div>

            <div class="admin-table">
              <div 
                v-for="res in filteredReservations" 
                :key="res.id" 
                class="data-row reservation-row"
                :class="{ 'is-selected': selectedReservation?.id === res.id }"
                @click="selectedReservation = res"
              >
                <div class="row-content">
                  <div class="row-main">
                    <div class="client-info">
                      <strong>{{ res.name }}</strong>
                      <span>{{ res.email }}</span>
                    </div>
                    <div class="visit-info">
                      <span class="date">{{ res.date }}</span>
                      <span class="time">{{ res.time }}</span>
                      <span class="guests">{{ res.guests }} Ospiti</span>
                    </div>
                    <span :class="['status-pill', res.status]">{{ res.status === 'pending' ? 'In Attesa' : (res.status === 'confirmed' ? 'Confermata' : 'Annullata') }}</span>
                  </div>
                </div>
              </div>
              <div v-if="filteredReservations.length === 0" class="empty-state">
                <span class="icon">📭</span>
                <p>Al momento il registro è vuoto.</p>
              </div>
            </div>
          </section>

          <section v-if="activeTab === 'menu'" class="dash-content">
            <div class="content-actions">
              <h3>La Nostra Carta</h3>
              <button class="btn-add" @click="openAddMenu">+ Aggiungi Piatto</button>
            </div>
            <div class="admin-table menu-admin-table">
              <div v-for="item in menuItems" :key="item.id" class="data-row no-click menu-item-grid">
                <div class="item-thumbnail" v-if="item.image_url">
                  <img :src="item.image_url" :alt="item.name" />
                </div>
                <div class="item-thumbnail placeholder" v-else>
                  <span>☕</span>
                </div>
                
                <div class="item-info">
                  <strong>{{ item.name }}</strong>
                  <span class="category">{{ item.category }}</span>
                </div>
                
                <div class="item-desc">
                  {{ item.description }}
                </div>
                
                <div class="item-price">
                  €{{ item.price.toFixed(2) }}
                </div>
                
                <div class="item-actions">
                  <button class="btn-edit" @click="openEditMenu(item)">Modifica</button>
                  <button class="btn-delete" @click="deleteMenuItem(item.id)">Elimina</button>
                </div>
              </div>
            </div>
          </section>
        </div>

        <aside class="detail-panel" v-if="activeTab === 'reservations'">
          <div v-if="selectedReservation" class="panel-inner animate-slide-in">
            <div class="panel-header">
              <span :class="['status-pill', selectedReservation.status]">{{ selectedReservation.status === 'pending' ? 'In Attesa' : (selectedReservation.status === 'confirmed' ? 'Confermata' : 'Annullata') }}</span>
              <h2>Dettagli Prenotazione</h2>
            </div>

            <div class="detail-section">
              <label>Informazioni Ospite</label>
              <div class="detail-card">
                <h3>{{ selectedReservation.name }}</h3>
                <p>{{ selectedReservation.email }}</p>
                <p>{{ selectedReservation.phone }}</p>
              </div>
            </div>

            <div class="detail-section">
              <label>Programmazione</label>
              <div class="detail-grid">
                <div class="grid-item">
                  <small>Date</small>
                  <p>{{ selectedReservation.date }}</p>
                </div>
                <div class="grid-item">
                  <small>Time</small>
                  <p>{{ selectedReservation.time }}</p>
                </div>
                <div class="grid-item">
                  <small>Ospiti</small>
                  <p>{{ selectedReservation.guests }} Persone</p>
                </div>
              </div>
            </div>

            <div class="detail-section" v-if="selectedReservation.ordered_items">
              <label>Selezione Pre-Ordine</label>
              <div class="order-list">
                <div v-for="item in JSON.parse(selectedReservation.ordered_items)" :key="item.name" class="order-item">
                  <span class="qty">{{ item.qty }}x</span>
                  <span class="name">{{ item.name }}</span>
                </div>
              </div>
            </div>

            <div class="panel-footer">
              <div v-if="selectedReservation.status === 'pending'" class="action-group">
                <button @click="confirmAction('confirmed')" class="btn-primary">Approva Prenotazione</button>
                <button @click="confirmAction('cancelled')" class="btn-outline-danger">Annulla</button>
              </div>
              <div v-else class="action-group revision">
                <p class="status-note">Questa prenotazione è <strong>{{ selectedReservation.status === 'confirmed' ? 'Confermata' : 'Annullata' }}</strong>.</p>
                <button @click="confirmAction(selectedReservation.status === 'confirmed' ? 'cancelled' : 'confirmed')" class="btn-text">
                  Vuoi cambiarla in {{ selectedReservation.status === 'confirmed' ? 'Annullato' : 'Confermato' }}?
                </button>
              </div>
            </div>
          </div>
          <div v-else class="panel-empty">
            <span class="icon">👈</span>
            <p>Seleziona una prenotazione per visualizzare i dettagli completi e i piatti pre-ordinati.</p>
          </div>
        </aside>
      </div>
    </main>

    <!-- Confirmation Overlay -->
    <div v-if="showConfirm" class="modal-overlay" @click="showConfirm = false">
      <div class="confirm-modal animate-slide-in" @click.stop>
        <div class="modal-icon">{{ pendingStatus === 'confirmed' ? '✅' : '❌' }}</div>
        <h3>{{ pendingStatus === 'confirmed' ? 'Conferma Prenotazione' : 'Annulla Prenotazione' }}</h3>
        <p>Sei sicuro di voler segnare questa prenotazione come <strong>{{ pendingStatus === 'confirmed' ? 'Confermata' : 'Annullata' }}</strong>?</p>
        <div class="modal-buttons">
          <button @click="executeStatusChange" :class="['btn-confirm', pendingStatus]">
            Sì, {{ pendingStatus === 'confirmed' ? 'Approva' : 'Annulla' }}
          </button>
          <button @click="showConfirm = false" class="btn-cancel">Indietro</button>
        </div>
      </div>
    </div>
    <!-- Menu Modal -->
    <div v-if="showMenuModal" class="modal-overlay" @click="showMenuModal = false">
      <div class="confirm-modal menu-modal animate-slide-in" @click.stop>
        <h3>{{ isEditing ? 'Modifica Piatto' : 'Aggiungi al Menu' }}</h3>
        <div class="form-grid">
          <div class="form-group">
            <label>Nome del Piatto</label>
            <input v-model="currentItem.name" placeholder="Es. Tortelli Verdi" />
          </div>
          <div class="form-group">
            <label>Categoria</label>
            <select v-model="currentItem.category">
              <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
          </div>
          <div class="form-group full">
            <label>Descrizione</label>
            <textarea v-model="currentItem.description" placeholder="Descrivi il piatto e gli ingredienti..."></textarea>
          </div>
          <div class="form-group">
            <label>Prezzo (€)</label>
            <input type="number" step="0.5" v-model.number="currentItem.price" />
          </div>
          <div class="form-group">
            <label>URL Immagine (Opzionale)</label>
            <input v-model="currentItem.image_url" placeholder="https://..." />
          </div>
        </div>
        <div class="modal-buttons">
          <button @click="saveMenuItem" class="btn-confirm confirmed">Salva Modifiche</button>
          <button @click="showMenuModal = false" class="btn-cancel">Annulla</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-dashboard {
  display: flex;
  height: 100vh;
  background: #fdfcfb;
  color: #2c2c2c;
  overflow: hidden;
}

/* Sidebar */
.sidebar {
  width: 300px;
  background: #fff;
  border-right: 1px solid #e5e0d8;
  display: flex;
  flex-direction: column;
  padding: 40px;
  z-index: 10;
}

.brand-box { margin-bottom: 60px; }
.logo { 
  font-size: 1.4rem; 
  font-weight: 800; 
  letter-spacing: 2px;
  font-family: var(--font-serif);
}
.accent { color: var(--primary); }
.staff-tag {
  font-size: 0.6rem;
  letter-spacing: 3px;
  color: var(--text-soft);
  margin-top: 5px;
  font-weight: 700;
}

.side-nav { flex-grow: 1; }
.side-nav button {
  width: 100%;
  text-align: left;
  border: none;
  background: none;
  padding: 18px 20px;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 12px;
  color: #666;
  display: flex;
  align-items: center;
  gap: 15px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.side-nav button:hover {
  background: #f9f7f5;
  color: var(--secondary);
}

.side-nav button.active {
  background: #fdf2f2;
  color: var(--primary);
  box-shadow: 0 4px 15px rgba(184, 45, 45, 0.1);
}

.notif-badge {
  background: var(--primary);
  color: #fff;
  font-size: 0.7rem;
  padding: 2px 8px;
  border-radius: 50px;
  margin-left: auto;
}

.sidebar-footer {
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.user-pill {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 15px;
}

.avatar {
  width: 32px;
  height: 32px;
  background: var(--secondary);
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.8rem;
}

.btn-logout {
  background: none;
  border: none;
  color: #e74c3c;
  font-weight: 700;
  width: 100%;
  text-align: left;
  padding: 10px 0;
  cursor: pointer;
  font-size: 0.9rem;
}

/* Main Layout */
.admin-main {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.admin-header {
  padding: 60px 60px 40px;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  border-bottom: 1px solid #f0eee9;
}

.header-left h1 {
  font-size: 2.8rem;
  font-family: var(--font-serif);
  margin-bottom: 10px;
}

.header-left h1 span {
  font-style: italic;
  color: var(--primary);
}

.header-left p {
  color: var(--text-soft);
  font-size: 1.1rem;
}

.admin-grid {
  display: flex;
  flex-grow: 1;
  overflow: hidden;
}

.main-content-area {
  flex-grow: 1;
  overflow-y: auto;
  padding: 40px 60px;
}

.dash-content {
  max-width: 1000px;
}

.detail-panel {
  width: 450px;
  background: #fff;
  border-left: 1px solid #e5e0d8;
  overflow-y: auto;
  box-shadow: -10px 0 30px rgba(0,0,0,0.02);
}

/* Table Design */
.data-row {
  background: #fff;
  padding: 24px;
  border-radius: 16px;
  margin-bottom: 15px;
  cursor: pointer;
  border: 1px solid #f0eee9;
  transition: all 0.3s;
}

.data-row:hover:not(.no-click) {
  border-color: var(--primary);
  transform: translateX(4px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.03);
}

.data-row.is-selected {
  border-color: var(--primary);
  background: #fdf2f2;
}

.row-main {
  display: flex;
  align-items: center;
  gap: 30px;
}

.client-info { width: 250px; }
.client-info strong { display: block; font-size: 1.1rem; margin-bottom: 4px; }
.client-info span { font-size: 0.85rem; color: #999; }

.visit-info {
  display: flex;
  gap: 20px;
}

.visit-info span {
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--secondary);
}

/* Status Pills */
.status-pill {
  font-size: 0.65rem;
  text-transform: uppercase;
  font-weight: 800;
  padding: 6px 14px;
  border-radius: 50px;
  letter-spacing: 1px;
}
.status-pill.pending { background: #fff8e1; color: #ffa000; }
.status-pill.confirmed { background: #e8f5e9; color: #2e7d32; }
.status-pill.cancelled { background: #ffebee; color: #c62828; }

/* Detail Panel Styling */
.panel-inner {
  padding: 60px 40px;
}

.panel-header {
  margin-bottom: 40px;
}

.panel-header h2 {
  font-family: var(--font-serif);
  font-size: 2rem;
  margin-top: 15px;
}

.detail-section {
  margin-bottom: 40px;
}

.detail-section label {
  display: block;
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--text-soft);
  letter-spacing: 2px;
  margin-bottom: 15px;
}

.detail-card {
  padding: 30px;
  background: #fdfaf7;
  border-radius: 12px;
  border: 1px solid #eee5da;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.grid-item {
  padding: 15px;
  background: #fdfaf7;
  border-radius: 12px;
  border: 1px solid #eee5da;
  text-align: center;
}

.grid-item small { display: block; font-size: 0.65rem; color: #999; margin-bottom: 5px; }
.grid-item p { font-weight: 800; font-size: 1rem; color: var(--secondary); }

.order-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.order-item {
  display: flex;
  justify-content: space-between;
  padding: 15px 20px;
  background: #fff;
  border: 1px solid #f0eee9;
  border-radius: 10px;
}

.order-item .qty { font-weight: 800; color: var(--primary); }
.order-item .name { font-weight: 600; color: var(--secondary); }

.panel-footer {
  margin-top: 60px;
  padding-top: 30px;
  border-top: 2px dashed #eee5da;
}

.action-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.btn-primary {
  background: var(--primary);
  color: #fff;
  border: none;
  padding: 20px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
}

.btn-outline-danger {
  background: none;
  border: 1px solid #ffebee;
  color: #c62828;
  padding: 18px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
}

.status-note { font-size: 0.9rem; color: var(--text-soft); text-align: center; margin-bottom: 5px; }
.btn-text { background: none; border: none; color: var(--primary); font-weight: 700; cursor: pointer; text-decoration: underline; width: 100%; }

.panel-empty {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  text-align: center;
  color: var(--text-soft);
}

.panel-empty .icon { font-size: 3rem; margin-bottom: 20px; }

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.6);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.confirm-modal {
  background: #fff;
  padding: 50px;
  border-radius: 24px;
  max-width: 450px;
  width: 90%;
  text-align: center;
  box-shadow: 0 40px 100px rgba(0,0,0,0.4);
}

.modal-icon { font-size: 3rem; margin-bottom: 20px; }

.confirm-modal h3 {
  font-family: var(--font-serif);
  font-size: 1.8rem;
  margin-bottom: 15px;
}

.confirm-modal p {
  color: var(--text-soft);
  line-height: 1.6;
  margin-bottom: 30px;
}

.modal-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.btn-confirm {
  padding: 18px;
  border-radius: 12px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  color: #fff;
}

.btn-confirm.confirmed { background: var(--secondary); }
.btn-confirm.cancelled { background: #c62828; }

.btn-cancel {
  background: #f0f0f0;
  border: none;
  padding: 18px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
}

/* Menu Items Styles */
.menu-admin-table {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.menu-item-grid {
  display: grid !important;
  grid-template-columns: 70px 220px 1fr 100px 180px;
  align-items: center;
  gap: 20px;
  padding: 16px 24px !important;
  margin-bottom: 0 !important;
}

.item-thumbnail {
  width: 70px;
  height: 70px;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--border);
  background: var(--bg-soft);
}

.item-thumbnail img { width: 100%; height: 100%; object-fit: cover; }
.item-thumbnail.placeholder { display: flex; align-items: center; justify-content: center; font-size: 1.8rem; }

.item-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.item-info strong { font-size: 1.15rem; color: var(--secondary); line-height: 1.2; }
.item-info .category { font-size: 0.75rem; text-transform: uppercase; color: var(--primary); font-weight: 800; letter-spacing: 0.5px; }

.item-desc {
  color: var(--text-soft);
  font-size: 0.9rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-price {
  font-weight: 800;
  font-size: 1.25rem;
  color: var(--secondary);
  text-align: right;
  font-family: var(--font-serif);
}

.item-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.btn-edit, .btn-delete {
  padding: 10px 16px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.85rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.btn-edit { background: #f0f0f0; color: var(--secondary); }
.btn-edit:hover { background: var(--secondary); color: white; transform: translateY(-2px); }

.btn-delete { background: #fff1f1; color: #c62828; }
.btn-delete:hover { background: #fee2e2; color: #b91c1c; transform: translateY(-2px); }

.btn-add {
  background: var(--secondary);
  color: #fff;
  border: none;
  padding: 14px 30px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
  box-shadow: var(--shadow-soft);
}

.btn-add:hover { background: var(--primary); transform: translateY(-3px); box-shadow: var(--shadow-md); }

/* Form Styles */
.menu-modal { max-width: 600px !important; }
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  text-align: left;
  margin-bottom: 30px;
}

.form-group.full { grid-column: span 2; }
.form-group label { display: block; font-size: 0.75rem; font-weight: 700; color: var(--text-soft); margin-bottom: 8px; text-transform: uppercase; }
.form-group input, .form-group select, .form-group textarea {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid var(--border);
  font-family: inherit;
  font-size: 0.95rem;
}

.form-group textarea { height: 100px; resize: none; }

.animate-slide-in {
  animation: slideInRight 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
}

@keyframes slideInRight {
  from { opacity: 0; transform: translateX(30px); }
  to { opacity: 1; transform: translateX(0); }
}

@media (max-width: 1200px) {
  .menu-item-row .row-main { flex-direction: column; align-items: flex-start; gap: 15px; }
  .item-desc { padding: 0; max-width: 100%; }
  .item-price { text-align: left; }
}
</style>
