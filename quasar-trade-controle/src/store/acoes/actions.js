import vue from 'vue'
import { acoes } from '../../graphql/acoes.js'

const loadAcoes = ({ commit }) => {
  vue.prototype.$apollo.query({
    query: acoes
  })
    .then(resp => resp.data.acoes)
    .then(acoes => commit('SET_ACOES', acoes))
    .catch(error => console.log(error))
}

export {
  loadAcoes
}
