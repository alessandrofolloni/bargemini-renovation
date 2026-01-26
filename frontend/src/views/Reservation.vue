<script setup>
import { ref } from 'vue'
import axios from 'axios'
import interiorImg from '../assets/interior.png'

const reservation = ref({
  name: '',
  email: '',
  phone: '',
  date: '',
  time: '',
  guests: 2
})

const submitReservation = async () => {
  try {
    await axios.post('http://localhost:8000/api/reservations', reservation.value)
    alert('Thank you! Your reservation is being processed.')
    reservation.value = { name: '', email: '', phone: '', date: '', time: '', guests: 2 }
  } catch (error) {
    alert('Something went wrong. Please call us directly.')
  }
}
</script>

<template>
  <div class="page-container">
    <section class="booking-hero">
      <div class="container hero-split">
        <div class="hero-left">
          <h1>Perfect <span>Moments</span>.</h1>
          <p>Book your table for breakfast, lunch, or our signature aperitivo.</p>
          <div class="contact-details">
            <div class="contact-item">
              <strong>Location</strong>
              <p>Via Roma, 12, Reggio Emilia</p>
            </div>
            <div class="contact-item">
              <strong>Phone</strong>
              <p>+39 0522 123456</p>
            </div>
          </div>
        </div>
        
        <div class="hero-right">
          <div class="booking-form-card fade-up">
            <h2>Reserve Now</h2>
            <form @submit.prevent="submitReservation" class="modern-form">
              <input v-model="reservation.name" type="text" placeholder="Full Name" required />
              <input v-model="reservation.email" type="email" placeholder="Email Address" required />
              <div class="form-row">
                <input v-model="reservation.phone" type="tel" placeholder="Phone" required />
                <input v-model="reservation.guests" type="number" placeholder="Guests" required />
              </div>
              <div class="form-row">
                <input v-model="reservation.date" type="date" required />
                <input v-model="reservation.time" type="time" required />
              </div>
              <button type="submit" class="btn-submit">Request Table</button>
            </form>
          </div>
        </div>
      </div>
    </section>

    <div class="decoration-img">
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

h1 {
  font-size: 5rem;
  letter-spacing: -3px;
  line-height: 1;
}

h1 span {
  color: var(--primary);
}

.hero-left p {
  font-size: 1.25rem;
  color: var(--text-soft);
  margin: 30px 0;
}

.contact-details {
  display: grid;
  gap: 20px;
  margin-top: 50px;
}

.contact-item strong {
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 2px;
  color: var(--primary);
}

.booking-form-card {
  background: #fff;
  padding: 60px;
  border-radius: var(--radius-lg);
  box-shadow: 0 40px 100px rgba(0,0,0,0.08);
}

.booking-form-card h2 {
  margin-bottom: 30px;
  font-size: 2rem;
}

.modern-form {
  display: grid;
  gap: 15px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

input {
  width: 100%;
  padding: 18px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 1rem;
  box-sizing: border-box;
}

.btn-submit {
  background: var(--text-main);
  color: #fff;
  padding: 20px;
  border: none;
  border-radius: var(--radius-sm);
  font-weight: 700;
  font-size: 1rem;
  margin-top: 20px;
}

.decoration-img {
  width: 100%;
  height: 400px;
  overflow: hidden;
}

.decoration-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

@media (max-width: 968px) {
  .hero-split { grid-template-columns: 1fr; gap: 60px; }
  .booking-form-card { padding: 40px; }
  h1 { font-size: 3.5rem; }
}
</style>
