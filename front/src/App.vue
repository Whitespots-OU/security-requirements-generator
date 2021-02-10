<template>
  <div id="app">
    <header class="ml-auto mr-auto pr-md-0 pl-md-0">
      <div class="container mt-3">
        <div class="row justify-content-between align-items-center">
          <a href='/' class="d-flex align-items-center top-link">
            <img src="@/assets/img/logo.svg" alt="logo">
            <div class="ml-3 logo-text d-none d-md-block">
              <div class="logo-title">Whitespots.io</div>
              <div class="logo-subtitle">{{ $t('Security requirements generator') }}</div>
            </div>
          </a>

          <div class="d-flex align-items-center mb-1">
            <div class="mb-1">
              <span class="languges" :class="{ 'languges-active': $i18n.locale === 'en' }" @click="selectLang('en')">EN</span>
              <span class="languges" :class="{ 'languges-active': $i18n.locale === 'ru' }" @click="selectLang('ru')">RU</span>
            </div>
            <a href="https://whitespots.io/security-assessment" target="_blank" class="btn-outline-red pt-1 pb-1">{{ $t('Security Assessment') }}</a>
          </div>
        </div>
      </div>
    </header>

    <router-view/>
  </div>
</template>

<script>
import { i18n } from './i18n'

export default {
  methods: {
    selectLang: function (locale) {
      this.$i18n.locale  = locale
      localStorage.setItem('locale', locale)

      const to = this.$router.resolve({ params: {locale} })
      this.$router.push(to.location)
      this.$router.go()
    },
  },
  created: function () {
    let locale = localStorage.getItem("locale")
    if (!Object.keys(i18n.messages).includes(locale))
      locale = i18n.fallbackLocale

    this.$i18n.locale  = locale
  },
}
</script>

<style lang="scss">
@import "assets/css/style.css";
</style>
