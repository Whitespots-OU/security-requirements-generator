<template>
  <main class="p-0 pb-5">
    <div class="container" v-if="requirement">
      <div class="row p-md-0 security-row">
        <div class="card w-100 mt-3 mt-md-5 pl-1 pl-md-2">
          <div class="col-12 col-md-8 security-card">
            <h2 class="card-title">{{ requirement.title }}</h2>
            <p class="p-text">
              <vue-simple-markdown :source="requirement.text"></vue-simple-markdown>
            </p>
            <h3 class="ul-title" v-if="requirement && requirement.test_cases.length">{{ $t('Test cases') }}</h3>
            <ul class="card-list sec-list" v-if="requirement && requirement.test_cases.length">
              <li class="card-list--item pl-1" v-for="testCase in requirement.test_cases">
                <h4 class="li-title">{{ testCase.title }}</h4>
                <p class="p-text">
                  <vue-simple-markdown :source="testCase.text"></vue-simple-markdown>
                </p>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>


<script>
import * as axios from 'axios'

export default {
  name: 'RequirementPage',
  data() {
    return {
      requirement: null
    }
  },
  created: function() {
    axios
        .get(`requirement/${this.$route.params.requirementId}`)
        .then(response => {
          this.requirement = response.data
        })
        .catch(error => {
          switch (error.response.status) {
            case 404: {
              this.$router.push({ name: 'Page404' })
              break;
            }
          }
        })
  }
}
</script>
