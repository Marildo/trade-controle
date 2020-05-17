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
    lancamentos: [],
  },

  getters: {
    isMenuVisible: (state) => state.isMenuVisible,
    tiposLancamentos: (state) => state.tiposLancamentos,
    carteiras: (state) => state.carteiras,
    carteira: (state) => state.carteira,
    patrimonio: (state) => state.patrimonio,
    acoes: (state) => state.acoes,
    lancamentos: (state) => state.lancamentos.map(formaterLancamento)
  },

  mutations: {
    toggleMenu: (state, isVisible) => state.isMenuVisible = isVisible === undefined ? !state.isMenuVisible : isVisible,
    tiposLancamentos: (state, payload) => state.tiposLancamentos = payload,
    carteiras: (state, payload) => state.carteiras = payload,
    carteira: (state, payload) => state.carteira = payload,
    patrimonio: (state, payload) => state.patrimonio = payload,
    acoes: (state, payload) => state.acoes = payload,
    lancamentos: (state, payload) => state.lancamentos = payload,
  },

  actions: {
    addAcao(context, payload) {
      const acoes = context.state.acoes
      const find = acoes.filter(a => a.codigo == payload.codigo)
      if (find.length === 0) {
        acoes.push(payload);
        context.commit('acoes', acoes)
      }
    },

    addCarteira(context, payload) {
      const carteiras = context.state.carteiras.push(payload)
      context.commit('carteiras',carteiras)
    },

    setIdCarteira(context, payload) {
      const carteira = context.state.carteiras.filter(i => i.id == payload)[0]
      context.commit('carteira', carteira)
    },
    
    carteiras(context, payload) {
      context.commit('carteiras', payload)
      const total = payload.map(c => c.saldoCaixa + c.saldoAcoes).reduce((c, n) => c + n)
      context.commit('patrimonio', total)
    },

    addLancamento(context, payload){
      const lancamentos = context.state.lancamentos
      lancamentos.push(payload)
      context.commit('lancamentos',lancamentos)
    },

    updateCarteira(context, payload) {
      context.commit('carteira', payload)
      const carteiras = context.state.carteiras
      const index = carteiras.findIndex(i => i.id == payload.id)
      carteiras.splice(index, 1, payload)
      context.dispatch('carteiras', carteiras)
    }
  },

  modules: {
  }

})
