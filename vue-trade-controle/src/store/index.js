import Vue from 'vue'
import Vuex from 'vuex'
import { formaterReal, formaterPercent } from "@/lib/numberUtils"

import { loadCarteira } from "@/controllers/carteiraController";

Vue.use(Vuex)

const formaterLancamento = (item) => {
  return {
    ...item,
    valor: formaterReal(item.valor),
    dataMovimentacao: new Date(
      parseInt(item.dataMovimentacao)
    ).toLocaleString()
  }
}

const formaterPortifolio = (item) => {
  return {
    ...item,
    cotacao: formaterReal(item.cotacao),
    totalAtual: formaterReal(item.totalAtual),
    custoTotal: formaterReal(item.custoTotal),
    resultado: formaterReal(item.resultado),
    percentual: formaterPercent(item.percentual),
  };
}

export default new Vuex.Store({
  state: {
    isMenuVisible: true,
    tiposLancamentos: [],
    acoes: [],
    carteiras: [],
    carteira: {},
    patrimonio: {},
    lancamentos: [],
    portifolio:[]
  },

  getters: {
    isMenuVisible: (state) => state.isMenuVisible,
    tiposLancamentos: (state) => state.tiposLancamentos,
    carteiras: (state) => state.carteiras,
    carteira: (state) => state.carteira,
    patrimonio: (state) => state.patrimonio,
    acoes: (state) => state.acoes,
    lancamentos: (state) => state.lancamentos.map(formaterLancamento),
    portifolio: (state) => state.carteira.portifolio.map(formaterPortifolio)
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
      context.commit('carteiras', carteiras)
    },

    setIdCarteira(context, payload) {
      const carteira = context.state.carteiras.filter(i => i.id == payload)[0]
      if (carteira === undefined) {
        setTimeout(() =>  loadCarteira(payload), 1000);
      }else{
        context.commit('carteira', carteira)
      }
    },

    carteiras(context, payload) {
      context.commit('carteiras', payload)   
      context.dispatch('updatePatrimonio', payload)
    },

    addLancamento(context, payload) {
      const lancamentos = context.state.lancamentos
      lancamentos.push(payload)
      context.commit('lancamentos', lancamentos)
    },

    deleteLancamento(context, payload) {
      const lancamentos = context.state.lancamentos
      const index = lancamentos.findIndex(i => i.id == payload.id)
      lancamentos.splice(index,1)
      context.commit('lancamentos', lancamentos)
    },

    updateCarteira(context, payload) {
      context.commit('carteira', payload)
      const carteiras = context.state.carteiras
      const index = carteiras.findIndex(i => i.id == payload.id)
      carteiras.splice(index, 1, payload)
      context.dispatch('carteiras', carteiras)
    },

    updatePatrimonio(context, payload){
      // TODO TypeError: reduce of empty array with no initial value
      const totalAcoes = payload.map(c => c.saldoAcoes).reduce((c, n) => c + n)
      const totalCaixa = payload.map(c => c.saldoCaixa).reduce((c, n) => c + n)
      const total = totalAcoes + totalCaixa
      const patrimonio  ={
          total,
          totalAcoes,
          totalCaixa
      }
      context.commit('patrimonio',patrimonio)
    }
  },

  modules: {
  }

})
