import vue from 'vue'
import { acoes, newAcao } from '../../graphql/acoes.js'

// TODO - Criar metodo para tratar erros de forma generica

const loadAcoes = ({ commit }) => {
  vue.prototype.$apollo.query({
    query: acoes
  })
    .then(resp => resp.data.acoes)
    .then(acoes => commit('SET_ACOES', acoes))
    .catch(error => console.log(error))
}

const addAcao = (context, codigo) => {
  return new Promise((resolve, reject) => {
    vue.prototype.$apollo.mutate({
      mutation: newAcao,
      variables: { codigo }
    })
      .then(() => vue.prototype.$apollo.resetStore())
      .then(() => context.dispatch('loadAcoes'))
      .then(() => resolve(true))
      .catch(error => {
        console.log(error)
        if (error.networkError) {
          if (error.networkError.result.errors) {
            console.log(error.networkError.result.errors[0].message)
          }
        }
        reject(error)
      })
  })
}

export {
  loadAcoes,
  addAcao
}
