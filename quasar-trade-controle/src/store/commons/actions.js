import gql from 'graphql-tag'
import vue from 'vue'

const loadTiposLancamentos = ({ commit }) => {
  vue.prototype.$apollo.query({
    query: gql` query{
        tiposLancamentos{ key descricao isSaida}
    }`
  })
    .then(resp => resp.data.tiposLancamentos)
    .then(tipos => commit('SET_TIPOS_LANCAMENTOS', tipos))
    .catch(error => console.log(error))
}

export {
  loadTiposLancamentos
}
