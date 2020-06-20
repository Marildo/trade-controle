<template>
 <q-card>
    <q-toolbar class="shadow-2 rounded-borders">
      <q-tabs align="left"
        v-model="tab"
        class="text-blue-grey-9"
        inline-label
      >
        <q-tab name="dashboard" icon="analytics" :label="carteira.nome" />
        <q-tab name="portifolio" icon="view_sidebar" label="Portifólio" />
        <q-tab name="lancamentos" icon="list" label="Lançamentos" />
      </q-tabs>
      <q-space />
      <tTrade tipoTrade="compra" :carteira="carteira" />
      <tTrade tipoTrade="venda" :carteira="carteira" />
      <tTrade tipoTrade="dayTrade" :carteira="carteira" />
      <tNovoLancamento :carteira="carteira" />
    </q-toolbar>

    <q-tab-panels v-model="tab" animated>
      <q-tab-panel name="dashboard">
        <theader-carteira :header="carteira" />
      </q-tab-panel>

      <q-tab-panel name="portifolio">
        <tPortifolio />
      </q-tab-panel>

      <q-tab-panel name="lancamentos">
        <tLancamentos />
      </q-tab-panel>
    </q-tab-panels>
 </q-card>
</template>

<script>

import theaderCarteira from '../../components/carteiras/HeaderCarteira.vue'
import tPortifolio from '../../components/carteiras/Portifolio'
import tLancamentos from '../../components/lancamentos/Lancamentos'
import tTrade from '../../components/lancamentos/Trade.vue'
import tNovoLancamento from '../../components/lancamentos/NovoLancamento'

export default {
  name: 'Carteira',

  components: {
    theaderCarteira,
    tLancamentos,
    tPortifolio,
    tTrade,
    tNovoLancamento
  },

  data () {
    return {
      tab: 'dashboard'
    }
  },

  mounted () {
    this.$store.dispatch('carteiras/loadCarteira', this.$route.params.id)
    this.$store.dispatch('carteiras/loadLancamentos', this.$route.params.id)
    this.$store.dispatch('acoes/loadAcoes')
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
