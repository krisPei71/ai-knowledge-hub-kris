import type { Router } from 'vue-router'

const WHITE_LIST = ['/login']

export function setupGuard(router: Router) {
    router.beforeEach((to, _from, next) => {
        const token = localStorage.getItem('token')
        if (WHITE_LIST.includes(to.path)) {
            if (token && to.path === '/login') {
                return next('/dashboard')
            }
            return next()
        }
        if (!token) {
            return next(`/login?redirect=${encodeURIComponent(to.fullPath)}`)
        }
        next()
    })
}