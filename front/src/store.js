import Vue from 'vue'
import Vuex from 'vuex'

import * as axios from 'axios'

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        categories: [],
        selectedCategoriesIds: [],
    },
    mutations: {
        setCategoriesIds(state, ids) {
            state.selectedCategoriesIds = ids
        },
        loadCategories(state) {
            axios
                .get('category')
                .then(response => {state.categories = response.data.results})
                .catch(error => {
                    console.error(error)
                })
        },
    },
    actions: {
        loadCategories(context) {
            context.commit('loadCategories')
        },
        setCategoriesIds(context, ids) {
            context.commit('setCategoriesIds', ids)
        },
    },
    getters: {
        getCategories: state => {
            return state.categories
        },
        getSelectedCategoriesIds: state => {
            return state.selectedCategoriesIds
        },
    }
})


export default store