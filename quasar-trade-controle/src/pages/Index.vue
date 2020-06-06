<template>
  <q-page class="flex flex-center" @click="Dispach()">
    <q-btn >Dispach </q-btn>
    Patri:  {{patrimonio}}
    <hr/>
    Cart: {{carteiras}}
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
    }

  },

  methods: {
    Dispach () {
      this.$store.dispatch('patrimonio/setPatrimonio', { totalAcoes: 300 })

      this.$store.dispatch('carteiras/loadCarteiras')
    }
  }
}
</script>
