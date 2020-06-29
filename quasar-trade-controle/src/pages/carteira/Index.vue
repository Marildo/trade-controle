<template>
  <div>
    <q-toolbar>
      <tHeaderCarteira :header="sum" />
      <q-space />
      <tNovaCarteira />
    </q-toolbar>
    <div class="row">
      <div
        class="col-md-4 col-12"
        v-for="carteira in carteiras"
        :key="carteira.id"
      >
        <div class="carteira">
          <q-btn
            :to="getLink(carteira.id)"
            :label="carteira.nome"
            flat
            class="text-blue-8 text-h5 "
          />
          <div class="text-teal-5 text-h6">
            Caixa: {{ carteira.saldoCaixa | formaterReal}}
          </div>
          <div class="text-teal-5 text-h6">
            Ações: {{ carteira.saldoAtivos | formaterReal}}
          </div>
          <div class="text-teal-5 text-h6">
            Total: {{ carteira.saldoCaixa + carteira.saldoAtivos | formaterReal}}
          </div>
          <div><hr /></div>
          <div class="actions">
            <q-btn
              flat
              color="primary"
              icon="fas fa-eye"
              :to="getLink(carteira.id)"
            />
            <tTrade tipoTrade="compra" :carteira="carteira" />
            <tTrade tipoTrade="venda" :carteira="carteira" />
            <tTrade tipoTrade="dayTrade" :carteira="carteira" />
            <tNovoLancamento :carteira="carteira" />
          </div>
        </div>
      </div>
    </div>
    <div>
        <ve-line :data="chartData"></ve-line>
    </div>
  </div>
</template>

<script>
import tTrade from '../../components/lancamentos/Trade.vue'
import tNovaCarteira from '../../components/carteiras/NovaCarteira'
import tHeaderCarteira from '../../components/carteiras/HeaderCarteira.vue'
import tNovoLancamento from '../../components/lancamentos/NovoLancamento'
import VeLine from 'v-charts/lib/line.common'
import Vue from 'vue'

Vue.component(VeLine.name, VeLine)

export default {
  name: 'CateirasIndex',

  components: {
    tHeaderCarteira,
    tTrade,
    tNovaCarteira,
    tNovoLancamento
  },

  mounted () {
    this.$store.dispatch('carteiras/loadCarteiras')
    this.$store.dispatch('acoes/loadAcoes')
  },

  computed: {
    carteiras () {
      return this.$store.state.carteiras.all
    },
    sum () {
      return this.$store.state.carteiras.sum
    }
  },

  methods: {
    getLink (id) {
      return {
        name: 'Carteira',
        params: { id }
      }
    }
  },

  data () {
    return {
      chartData: {
        columns: ['date', 'cost', 'profit', 'growthRate', 'people'],
        rows: [
          { cost: 1523, date: '01/01', profit: 1523, growthRate: 0.12, people: 100 },
          { cost: 1223, date: '01/02', profit: 1523, growthRate: 0.345, people: 20 },
          { cost: 2123, date: '01/03', profit: 1523, growthRate: 0.7, people: 50 },
          { cost: 4123, date: '01/04', profit: 1523, growthRate: 0.31, people: 85 },
          { cost: 3123, date: '01/05', profit: 1523, growthRate: 0.12, people: 90 },
          { cost: 7123, date: '01/06', profit: 1523, growthRate: 0.65, people: 100 }
        ]
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
  margin: 0.5em;
  background: #e0e2e024;
  box-shadow: 1px 1px 1px 0px rgba(181, 199, 230, 1);
}
.actions {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
}
</style>
