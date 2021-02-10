<template>
  <main>
    <div class="container">
      <div class="ml-auto mr-auto text-center">
        <div class="number">404</div>
        <div class="number-title">{{ $t('Ooops!!!') }}</div>
        <div class="number-subtitle">{{ $t('THAT PAGE DOES NOT EXIST OR IS UNAVAILABLE') }}</div>
        <a href="/" class="cta cta-link">{{ $t('go back to home') }}</a>
      </div>
    </div>
  </main>
</template>


<script>
export default {
  name: 'NotFoundPage',
}
</script>
