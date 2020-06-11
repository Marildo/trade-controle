<template>
  <div class="row">
    <div class="col-12 text-h4 text-blue-grey-6">
      {{ carteira.nome }}
    </div>
    <theader-carteira :header="sum" />
  </div>
</template>

<script>

import theaderCarteira from '../../components/HeaderCarteira.vue'

export default {
  name: 'Carteira',

  components: {
    theaderCarteira
  },

  mounted () {
    this.$store.dispatch('carteiras/loadCarteira', this.$route.params.id)
  },

  computed: {
    sum () {
      return this.$store.state.carteiras.sum
    }
  }
}
</script>

<style scoped>

</style>
