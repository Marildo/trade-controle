<template>
  <q-page class="flex flex-center" @click="Dispach()">
    <q-btn >Dispach </q-btn>
    Patri:  {{patrimonio}}
    <hr/>
    Cart: {{carteiras}}
    <hr/>
    Acoes: {{acoes}}
  </q-page>
</template>

<script>
export default {
  name: 'PageIndex',

  computed: {
    patrimonio () {
      return this.$store.state.patrimonio.patrimonio
    },

    carteiras () {
      return this.$store.state.carteiras.all
    },

    acoes () {
      return this.$store.state.acoes.all
    }

  },

  methods: {
    Dispach () {
      this.$store.dispatch('patrimonio/setPatrimonio', { totalAcoes: 300 })

      this.$store.dispatch('carteiras/loadCarteiras')

      this.$store.dispatch('acoes/loadAcoes')
    }
  }
}
</script>
