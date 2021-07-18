<template>
  <main class="ml-auto mr-auto">
    <b-container>
      <div class="row row-cont pl-md-0 pr-md-0">
        <div class="col-md-6 col-sm-12 p-0 main-title">
          {{ $t('Define your app functionality') }}
        </div>
      </div>
      <div class="row">
        <div class="col-md-6 col-12 p-0 left-container">
          <div class="row row-cont pl-md-0 pr-md-0">
            <div class="col-md-5 col-12">
              <div class="input-cont d-flex align-items-center" v-for="(cat, index) in getCategories" v-if="index % 2 === 0">
                <b-form-checkbox
                    :key="index"
                    v-model="selected"
                    :value="cat.id"
                    switch
                    @change="toggle">
                  {{ cat.name }}
                </b-form-checkbox>
              </div>
            </div>
            <div class="col-md-5 col-12 right-input">
              <div class="input-cont d-flex align-items-center" v-for="(cat, index) in getCategories" v-if="index % 2 === 1">
                <b-form-checkbox
                    :key="index"
                    v-model="selected"
                    :value="cat.id"
                    switch
                    @change="toggle">
                  {{ cat.name }}
                </b-form-checkbox>
              </div>
            </div>
            <div class="col-md-5 col-12 pr-md-0 cta-cont">
              <router-link class="w-100 btn pt-md-4 pb-md-4 pt-3 pb-3 cta" :disabled="selected.length === 0"
                           :to="{ name: 'Export', params: { locale: this.$i18n.locale }}" tag="button">
                {{ $t('Get requirements') }}
              </router-link>
            </div>
          </div>
        </div>
        <div class="col-6 p-0 right-cont d-md-block d-none">
          <img src="@/assets/img/main-img.svg" alt="main">
        </div>
      </div>
    </b-container>
  </main>
</template>

<script>
import {mapGetters, mapActions} from 'vuex'

export default {
  name: 'HomePage',
  data() {
    return {
      selected: [],
      categories: [],
    }
  },
  computed: {
    ...mapGetters(['getCategories'])
  },
  created() {
    this.loadCategories()
    
    if (Array.isArray(this.$route.query.cat)) {
      let query = []
      this.$route.query.cat.forEach(cat => query.push(parseInt(cat)))
      let preset = query.filter(function (cat) { return  cat })
      preset.forEach(cat => this.selected.push(cat))
      this.setCategoriesIds(this.selected)
    }
    else if (this.$route.query.cat && parseInt(this.$route.query.cat)) {
      this.selected.push(parseInt(this.$route.query.cat))
      this.setCategoriesIds(this.selected)
    }
  },
  methods: {
    ...mapActions(['loadCategories', 'setCategoriesIds']),
    toggle() {
      this.setCategoriesIds(this.selected)
    }
  },
}
</script>

<style scoped>
</style>
