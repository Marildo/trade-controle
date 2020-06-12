<template>
 <q-card>
    <q-tabs align="left"
      v-model="tab"
      class="text-blue-grey-9"
      inline-label
      >
      <q-tab name="dashboard" icon="insert_chart" :label="carteira.nome" />
      <q-tab name="lancamentos" icon="list" label="Lançamentos" />
      <q-tab name="movies" icon="movie" label="Movies" />
    </q-tabs>

    <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="dashboard">
          <theaderCarteira :header="carteira" />
        </q-tab-panel>

        <q-tab-panel name="lancamentos">
          <tLancamentos />
        </q-tab-panel>

        <q-tab-panel name="movies">
          <div class="text-h6">Movies</div>
          Lorem ipsum dolor sit amet consectetur adipisicing elit.
        </q-tab-panel>
      </q-tab-panels>
 </q-card>
</template>

<script>

import theaderCarteira from '../../components/HeaderCarteira.vue'
import tLancamentos from '../../components/lancamentos/Lancamentos'

export default {
  name: 'Carteira',

  components: {
    theaderCarteira,
    tLancamentos
  },

  data () {
    return {
      tab: 'dashboard'
    }
  },

  mounted () {
    this.$store.dispatch('carteiras/loadCarteira', this.$route.params.id)
    this.$store.dispatch('carteiras/loadLancamentos', this.$route.params.id)
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
