import { ref } from 'vue'

// Shared (module-level) cookie-consent state, used by the banner in App.vue
// and the Google Maps embed in Home.vue.
export const cookieAccepted = ref(localStorage.getItem('cookieConsent') === 'yes')

export function acceptCookies() {
  localStorage.setItem('cookieConsent', 'yes')
  cookieAccepted.value = true
}
