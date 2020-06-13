<template>
  <div>
    <div class="row">
      <div class="col-md-4 col-12" v-for="carteira in carteiras" :key="carteira.id">
        <div class="carteira">
          <q-btn :to="getLink(carteira.id)" :label="carteira.nome" flat  class="text-blue-8 text-h5 "/>
          <div class="text-teal-5 text-h6">Caixa: {{carteira.saldoCaixa}}</div>
          <div class="text-teal-5 text-h6">Ações: {{carteira.saldoAcoes}}</div>
          <div class="text-teal-5 text-h6">Total: {{carteira.saldoCaixa + carteira.saldoAcoes}}</div>
          <div> <hr></div>
          <div class="actions">
            <q-btn flat color="primary" icon="fas fa-eye"  :to="getLink(carteira.id)" />
            <trade :isBuy=true  :carteira="carteira" />
            <trade :isBuy=false :carteira="carteira" />
            <q-btn flat color="orange" icon="fas fa-retweet" />
          </div>
        </div>
      </div>
     </div>
  </div>
</template>

<script>
import trade from '../../components/lancamentos/Trade.vue'
export default {
  name: 'CateirasIndex',

  components: {
    trade
  },

  mounted () {
    this.$store.dispatch('carteiras/loadCarteiras')
    this.$store.dispatch('acoes/loadAcoes')
  },

  computed: {
    carteiras () {
      return this.$store.state.carteiras.all
    }
  },

  methods: {
    getLink (id) {
      return {
        name: 'Carteira',
        params: { id }
      }
    }
  }
}
</script>

<style scoped>
  .carteira {
    display: flex;
    flex-direction: column;
    padding: 1em;
    margin: .5em;
    background: #eeffee;
    box-shadow: 1px 1px 1px 0px rgba(181,199,230,1);
  }
  .actions {
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
  }
</style>
