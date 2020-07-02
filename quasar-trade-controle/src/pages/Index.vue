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

    <hr/>
    Total carteiras : {{ sumCarteiras }}
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
    },

    sumCarteiras () {
      return this.$store.state.carteiras.sum
    }

  },

  methods: {
    Dispach () {
      this.$store.dispatch('carteiras/loadCarteiras')
    //  this.$store.dispatch('commons/loadTiposLancamentos')
      // this.$store.dispatch('patrimonio/setPatrimonio', { totalAcoes: 300 })
    }
  }
}
</script>
