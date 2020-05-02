import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isMenuVisible: true,
    tiposLancamentos: []
  },

  getters: {
    isMenuVisible: (state) => state.isMenuVisible,
    tiposLancamentos: (state) =>{
      return state.tiposLancamentos
    }
  },

  mutations: {
    toggleMenu(state, isVisible){      
        state.isMenuVisible =  isVisible === undefined ? !state.isMenuVisible : isVisible             
    },

    setTiposLancamentos(state, payload){      
      state.tiposLancamentos = payload    
    }
  },

  actions: {
  },

  modules: {
  }
})
