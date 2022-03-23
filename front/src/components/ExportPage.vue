<template>
  <main class="p-0">
    <b-container>
      <div class="row justify-content-between align-items-center main-row">
        <div class="col-fluid p-md-0 px-3">
          <button class="btn d-flex export cta py-md-3 px-md-4" v-if="!isResultSent && !isDone" @click="makeExport">
            {{ $t('Export') }}
          </button>

          <div class="wait d-flex align-items-start" v-if="isResultSent && !isDone">
            <img src="@/assets/img/wait.svg" alt="wait" class="wait-img">
            <div>
              <div class="message-title d-flex">{{ $t('In progress') }}</div>
              <div class="message-subtitle d-flex">{{ $t('Update in 10 sec') }}</div>
            </div>
          </div>

          <div class="load d-flex align-items-center" v-if="isDone">
            <a class="message-title d-md-block px-3" target="_blank" :href="'/media/exports/' + exportId + '.pdf'">
              <img src="@/assets/img/load.svg" alt="load" class="link-img">
              {{ $t('Download PDF') }}
            </a>
            <button type="button" class="btn btn-outline-red pt-1 pb-1 disabled-message" @click="exportAgain">
              {{ $t('Make export again') }}
            </button>
          </div>

          <div class="alert-cont d-flex align-items-start" v-if="hasError">
            <img src="@/assets/img/alert.svg" alt="alert" class="alert-img">
            <div>
              <div class="message-title">{{ $t('Failed') }}</div>
              <div class="message-subtitle">{{ $t('Something') }} <br class="d-md-none"> {{ $t('went wrong') }}</div>
            </div>
          </div>
        </div>

        <b-button variant="b-btn-outline-blue" class="btn float-right b-btn-outline-blue pt-1 pb-1 d-none d-md-block" @click="createURL($t('Success!'), $t('Link copied to the clipboard'))">
          {{ $t('Copy a link to these categories') }}
        </b-button>
      </div>

      <div class="row content-row">
        <div class="col-4 d-none d-md-block pl-0">
          <div class="card list-group" id="list">
            <a class="list-group-item list-group-item-action"
               v-for="(cat, index_cat) in getCategories"
               v-if="getSelectedCategoriesIds.includes(cat.id)"
               :href="'#cat-' + index_cat">
              {{ cat.name }}
            </a>
          </div>
          <div class="card disabled-card list-group">
            <a class="list-group-item list-group-item-action" style="cursor: default"
               v-for="(cat, index_cat) in getCategories"
               v-if="!getSelectedCategoriesIds.includes(cat.id)">
              {{ cat.name }}
            </a>
          </div>
        </div>
        <div class="col-12 col-md-8 pr-md-0 ">
          <div data-spy="scroll" data-target="#list" data-offset="0" class="sc">
            <div class="card" :id="'cat-' + index_cat" v-for="(cat, index_cat) in getCategories" v-if="getSelectedCategoriesIds.includes(cat.id)">
              <div class="col-12 col-md-8">
                <div class="card-title">{{ cat.name }}</div>
                <p class="p-text">
                  <vue-simple-markdown :source="cat.summary"></vue-simple-markdown>
                </p>
                <div class="card-group" v-for="(req, index_req) in cat.requirements">
                  <div class="d-flex align-items-center">
                    <b-form-checkbox
                        :key="index_req"
                        :model="getSelectedCategoriesIds[cat.id]"
                        @change="turnSwitcher($event, cat.id, req.id)"
                        :value="req.id"
                        switch>
                      <span v-b-popover.hover="$t('Mark requirement as passed')">{{ req.title }}</span>
                    </b-form-checkbox>
                  </div>
                  <button type="button" class="btn show-btn" v-b-modal="'requirementModal'" @click="loadRequirement(req.id)">
                    <img src="@/assets/img/info.svg" alt="info" class="info-img">
                    {{ $t('show details') }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </b-container>

    <b-modal id="requirementModal" @hidden="closeModal" :hide-footer="true" size="lg">
      <template #modal-title>{{ $t('Requirement') }}</template>

      <div class="col-12 security-card" v-if="JSON.stringify(currentRequirement) !== '{}'">
        <div class="d-flex justify-content-between align-items-start">
          <h2 class="card-title">{{ currentRequirement.title }}</h2>
        </div>

        <p class="p-text" v-if="currentRequirement.text">
          <vue-simple-markdown :source="currentRequirement.text"></vue-simple-markdown>
        </p>

        <div v-if="currentRequirement.test_cases.length">
          <h3 class="ul-title">{{ $t('Test cases') }}</h3>
          <ul class="card-list p-0 pl-3">
            <li class="card-list--item pl-2" v-for="(test_case, test_case_cat) in currentRequirement.test_cases">
              <h4 class="li-title">{{ test_case.title }}</h4>
              <p class="p-text">
                <vue-simple-markdown :source="test_case.text"></vue-simple-markdown>
              </p>
            </li>
          </ul>
        </div>
      </div>
    </b-modal>
  </main>
</template>


<script>
import * as axios from 'axios'
import {mapGetters} from 'vuex'
import {i18n} from '@/i18n'

export default {
  name: 'ExportPage',
  data() {
    return {
      selectedIds: [],
      selectedReq: {},
      isResultSent: false,
      hasError: false,
      isDone: false,
      exportId: null,
      currentRequirement: {},
      url: null
    }
  },
  computed: {
    ...mapGetters(['getCategories', 'getSelectedCategoriesIds'])
  },
  created() {
    if (this.getSelectedCategoriesIds.length === 0)
      this.$router.push({'name': 'Home'})

    this.getSelectedCategoriesIds.map((i) => { this.selectedReq[i] = []})
  },
  methods: {
    turnSwitcher: function($event, catId, reqId) {
      if ($event === false) {
        this.selectedReq[catId] = this.selectedReq[catId].filter((r) => { reqId !== r })
      }
      else {
        this.selectedReq[catId].push(reqId)
      }
    },
    makeExport: function () {
      let postData = []
      for (const catId of Object.keys(this.selectedReq))
        postData.push({"category_id": catId, "requirements_ids": this.selectedReq[catId]})

      let timeoutId;
      axios
          .post('export', {data: postData, language: this.$i18n.locale})
          .then(response => {
            this.isResultSent = true
            this.exportId = response.data.uuid

            let that = this
            timeoutId = setTimeout(function() {
              axios
                  .get(`export/${that.exportId}`)
                  .then(response => {
                    switch (response.data.status) {
                      case "finished": {
                        that.isDone = true
                        clearTimeout(timeoutId)
                        break
                      }
                      case "failed": {
                        that.isDone = false
                        that.isResultSent = true
                        that.hasError = true
                        clearTimeout(timeoutId)
                        break
                      }
                    }
                  })
                  .catch(error => {
                    console.error(error)
                  })
            }, 10000);
          })
          .catch(error => {
            this.hasError = false
            console.error(error)
          })
    },
    closeModal: function () {
      this.currentRequirement = {}
    },
    loadRequirement: function (reqId) {
      axios
          .get(`requirement/${reqId}`)
          .then(response => {
            this.currentRequirement = response.data
          })
          .catch(error => {
            console.error(error)
          })
    },
    exportAgain() {
      this.exportId = null
      this.isDone = false
      this.isResultSent = false
    },
    createURL(toastTitle, toastBody) {
      let selected_ids = []
      for (const catId of Object.keys(this.selectedReq))
        selected_ids.push(catId)
      let link = '/?cat='.concat(selected_ids.join("&cat="))
      this.url = window.location.origin.concat(link)
      navigator.clipboard.writeText(this.url)
      this.$bvToast.toast(`${toastBody}`, {
        title: `${toastTitle}`,
        toaster: `b-toaster-bottom-right`,
        solid: false,
        appendToast: true
      })
    } 
  },
}
</script>

<style scoped>
</style>
