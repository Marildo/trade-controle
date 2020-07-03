<template>
  <div>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'Carteiras',
  mounted () {
    this.$store.dispatch('carteiras/loadCarteiras')
    this.$store.dispatch('carteiras/loadHistoricoMensal')
    this.$store.dispatch('acoes/loadAcoes')
  }
}
</script>
