<template>
  <div class="row">
    <div class="col-12 text-h4 text-blue-grey-6">
      {{ carteira.nome }}
    </div>
    <div class="row 12" >
      <theaderCarteira :header="carteira" />
    </div>
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
    carteira () {
      return this.$store.state.carteiras.current
    }
  }
}
</script>

<style scoped>

</style>
