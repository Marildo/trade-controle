import Vue from 'vue'
import Vuex from 'vuex'
import { formateReal } from "@/lib/numberUtils"

Vue.use(Vuex)


const formaterLancamento = (item) => {
  return {
    ...item,
    valor: formateReal(item.valor),
    dataMovimentacao: new Date(
      parseInt(item.dataMovimentacao)
    ).toLocaleString()
  };
};


export default new Vuex.Store({
  state: {
    isMenuVisible: true,
    tiposLancamentos: [],
    acoes: [],
    carteiras: [],
    carteira: {},
    patrimonio: 0,
    lancamentos: []
  },

  getters: {
    isMenuVisible: (state) => state.isMenuVisible,
    tiposLancamentos: (state) => state.tiposLancamentos,
    carteiras: (state) => state.carteiras,
    getCarteira: (state) => state.carteira,
    patrimonio: (state) => state.patrimonio,
    acoes: (state) => state.acoes,
    lancamentos: (state) => state.lancamentos.map(formaterLancamento)
  },

  mutations: {
    toggleMenu(state, isVisible) {
      state.isMenuVisible = isVisible === undefined ? !state.isMenuVisible : isVisible
    },

    setTiposLancamentos(state, payload) {
      state.tiposLancamentos = payload
    },

    setCarteiras: (state, payload) => state.carteiras = payload,
    setCarteira: (state, payload) => state.carteira = payload,
    setPatrimonio: (state, payload) => state.patrimonio = payload,
    setAcoes: (state, payload) => state.acoes = payload,
    setLancamentos: (state, payload) => state.lancamentos = payload
  },

  actions: {
    setCarteira(context, payload) {
      const carteira = context.state.carteiras.filter(i => i.id == payload)[0]
      context.commit('setCarteira', carteira)
    },

    setCarteiras(context, payload) {
      context.commit('setCarteiras', payload)
      const total = payload.map(c => c.saldoCaixa + c.saldoAcoes).reduce((c, n) => c + n)
      context.commit('setPatrimonio', total)
    },

    addLancamento(context, payload) {
      context.state.lancamentos.push(payload)
    },

    setLancamentos(context, payload) {
      context.commit('setLancamentos', payload)
    },

    updateCarteira(context, payload) {
      context.commit('setCarteira', payload)
      const carteiras = context.state.carteiras
      const index = carteiras.findIndex(i => i.id == payload.id)
      carteiras.splice(index, 1, payload)
      context.dispatch('setCarteiras', carteiras)
    }
  },

  modules: {
  }
})
