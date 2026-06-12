import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import About from './views/About.vue'
import Menu from './views/Menu.vue'
import Reservation from './views/Reservation.vue'
import Login from './views/Login.vue'
import Admin from './views/Admin.vue'
import Privacy from './views/Privacy.vue'

const routes = [
    { path: '/', component: Home },
    { path: '/about', component: About },
    { path: '/menu', component: Menu },
    { path: '/reservation', component: Reservation },
    { path: '/privacy', component: Privacy },
    { path: '/login', component: Login },
    {
        path: '/admin',
        component: Admin,
        beforeEnter: (to, from, next) => {
            const token = localStorage.getItem('token')
            if (token) next()
            else next('/login')
        }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior() {
        return { top: 0 }
    }
})

export default router
