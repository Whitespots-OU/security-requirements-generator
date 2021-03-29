import Vue from 'vue'
import axios from 'axios'
import VueAxiosPlugin from 'vue-axios-plugin'

import { i18n } from '../i18n'

axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.baseURL = `/api/v1`
axios.interceptors.request.use((config) => {
    if (!config.url.endsWith('/'))
        config.url += '/'

    config.headers.common["ACCEPT-LANGUAGE"] = i18n.locale

    return config
}, (error) => {
    return Promise.reject(error)
});
Vue.prototype.$axios = axios;

Vue.use(VueAxiosPlugin, {})
