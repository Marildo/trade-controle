<template>
  <q-page class="flex flex-center" @click="Dispach()">
    <q-btn >Dispach </q-btn>
    Patri:  {{patrimonio}}
    <hr/>
    Cart: {{carteiras}}
    <hr/>
    Acoes: {{acoes}}

    <hr/>
    Tipos: {{tiposLancamentos}}
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
    },

    tiposLancamentos () {
      return this.$store.state.commons.tiposLancamentos
    }

  },

  methods: {
    Dispach () {
      // this.$store.dispatch('patrimonio/setPatrimonio', { totalAcoes: 300 })

      // this.$store.dispatch('carteiras/loadCarteiras')

      // this.$store.dispatch('acoes/loadAcoes')

      this.$store.dispatch('commons/loadTiposLancamentos')
    }
  }
}
</script>
