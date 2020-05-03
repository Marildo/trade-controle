import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isMenuVisible: true,
    tiposLancamentos: [],
    carteiras: [],
    carteira:{}
  },

  getters: {
    isMenuVisible: (state) => state.isMenuVisible,
    tiposLancamentos: (state) => state.tiposLancamentos,
    getCarteiras: (state) => state.carteiras,
    getCarteira: (state) => state.carteira,
  },

  mutations: {
    toggleMenu(state, isVisible) {
      state.isMenuVisible = isVisible === undefined ? !state.isMenuVisible : isVisible
    },

    setTiposLancamentos(state, payload) {
      state.tiposLancamentos = payload
    },

    setCarteiras: (state, payload) => state.carteiras = payload,
    setCarteira: (state, payload) => state.carteira = payload
  },

  actions: {
      setCarteira(context, payload) {
         const carteira = context.state.carteiras.filter( i => i.id == payload)[0] 
         context.commit('setCarteira',carteira)       
      },

      updateCarteira(context ,payload){
        context.commit('setCarteira',payload) 
        const carteiras =  context.state.carteiras
        const index = carteiras.findIndex( i => i.id == payload.id)
        carteiras.splice(index,1,payload)
        context.commit('setCarteiras',carteiras) 
      }
  },

  modules: {
  }
})
