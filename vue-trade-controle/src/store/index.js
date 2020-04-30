import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isMenuVisible: true
  },

  getters: {
    isMenuVisible: (state) => state.isMenuVisible
  },

  mutations: {
    toggleMenu(state, isVisible){      
        state.isMenuVisible =  isVisible === undefined ? !state.isMenuVisible : isVisible             
    }
  },

  actions: {
  },

  modules: {
  }
})
