<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const reservations = ref([])
const menuItems = ref([])
const router = useRouter()
const activeTab = ref('reservations')

const fetchAdminData = async () => {
  const token = localStorage.getItem('token')
  const config = { headers: { Authorization: `Bearer ${token}` } }
  
  try {
    const [resResp, menuResp] = await Promise.all([
      axios.get('http://localhost:8000/api/admin/reservations', config),
      axios.get('http://localhost:8000/api/menu')
    ])
    reservations.value = resResp.data
    menuItems.value = menuResp.data
  } catch (err) {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      router.push('/login')
    }
  }
}

const updateStatus = async (id, status) => {
  const token = localStorage.getItem('token')
  await axios.patch(`http://localhost:8000/api/admin/reservations/${id}?status=${status}`, {}, {
    headers: { Authorization: `Bearer ${token}` }
  })
  fetchAdminData()
}

const logout = () => {
  localStorage.removeItem('token')
  router.push('/')
}

onMounted(fetchAdminData)
</script>

<template>
  <div class="admin-dashboard">
    <div class="sidebar">
      <div class="logo">GEMINI <span class="highlight">ADMIN</span></div>
      <nav>
        <button :class="{active: activeTab === 'reservations'}" @click="activeTab = 'reservations'">Reservations</button>
        <button :class="{active: activeTab === 'menu'}" @click="activeTab = 'menu'">Menu Management</button>
      </nav>
      <button @click="logout" class="btn-logout">Logout</button>
    </div>

    <main class="content">
      <div v-if="activeTab === 'reservations'">
        <h2>Table Reservations</h2>
        <div class="res-list">
          <div v-for="res in reservations" :key="res.id" class="glass-card table-row">
            <div class="row-info">
              <h3>{{ res.name }}</h3>
              <p>{{ res.date }} at {{ res.time }} • {{ res.guests }} Guests</p>
              <span :class="['status-badge', res.status]">{{ res.status }}</span>
            </div>
            <div class="row-actions">
              <button v-if="res.status === 'pending'" @click="updateStatus(res.id, 'confirmed')" class="btn-small-confirm">Confirm</button>
              <button v-if="res.status !== 'cancelled'" @click="updateStatus(res.id, 'cancelled')" class="btn-small-cancel">Cancel</button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'menu'">
        <h2>Menu Management</h2>
        <div class="menu-list">
          <div v-for="item in menuItems" :key="item.id" class="glass-card table-row">
            <div class="row-info">
              <h3>{{ item.name }}</h3>
              <p>{{ item.category }} • €{{ item.price.toFixed(2) }}</p>
            </div>
            <div class="row-actions">
              <button class="btn-small-cancel">Edit</button>
              <button class="btn-small-cancel">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.admin-dashboard {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 280px;
  background: #111;
  padding: 2rem;
  display: flex;
  flex-direction: column;
}

nav { margin-top: 3rem; flex-grow: 1; }

nav button {
  display: block;
  width: 100%;
  text-align: left;
  background: none;
  border: none;
  color: var(--text-muted);
  padding: 1rem;
  font-size: 1.1rem;
  cursor: pointer;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

nav button.active { background: var(--glass); color: var(--primary); }

.content { flex-grow: 1; padding: 4rem; overflow-y: auto; }

.table-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding: 1.5rem;
}

.status-badge {
  font-size: 0.7rem;
  text-transform: uppercase;
  padding: 2px 8px;
  border-radius: 4px;
}
.status-badge.pending { background: #f39c12; color: #000; }
.status-badge.confirmed { background: #2ecc71; color: #000; }
.status-badge.cancelled { background: #e74c3c; color: white; }

.btn-small-confirm { background: #2ecc71; border: none; padding: 5px 15px; border-radius: 4px; cursor: pointer; margin-right: 0.5rem; }
.btn-small-cancel { background: #e74c3c; border: none; padding: 5px 15px; border-radius: 4px; color: white; cursor: pointer; }

.btn-logout { margin-top: auto; padding: 1rem; background: var(--glass); border: 1px solid var(--glass-border); color: white; border-radius: 8px; cursor: pointer; }
</style>
