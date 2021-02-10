import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from './components/HomePage.vue'
import Export from './components/ExportPage.vue'
import RequirementPage from './components/RequirementPage.vue'
import NotFoundPage from './components/NotFoundPage.vue'
import { i18n } from './i18n'

Vue.use(VueRouter)

const routes = [
  {
    path: '/:locale',
    component: {
      template: "<router-view></router-view>"
    },
    beforeEnter: (to, from, next) => {
      const locale = to.params.locale;
      localStorage.setItem("locale", locale)

      if (!Object.keys(i18n.messages).includes(locale))
        return next(i18n.fallbackLocale)

      i18n.locale = locale

      return next()
    },
    children: [
      {
        path: '',
        name: 'Home',
        component: Home
      },
      {
        path: 'export',
        name: 'Export',
        component: Export
      },
      {
        path: 'requirement/:requirementId',
        name: 'Requirement',
        component: RequirementPage
      },
      {
        path: '/404',
        component: NotFoundPage,
        name: 'Page404',
      },
    ],
  },
  {
    path: '/',
    redirect() {
      let locale = localStorage.getItem("locale")
      if (!Object.keys(i18n.messages).includes(locale))
        locale = i18n.fallbackLocale

      return locale
    }
  },
  {
    path: '/:pathMatch(.*)*',
    component: NotFoundPage,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
