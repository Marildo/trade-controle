import gql from 'graphql-tag'
import vue from 'vue'

import store from '@/store';
import { showToastSuccess, catchError } from '@/lib/messages'

export {
  loadCarteiras,
  loadCarteira,
  saveCarteira,
  setCarteira
}

const loadCarteiras = () => {
  return vue.prototype.$api.query({
    query: gql`
          query{
            carteiras {
              id nome saldoCaixa saldoAcoes
            }
          }`
  })
    .then(resp => resp.data.carteiras)
    .then(carteiras => setCarteiras(carteiras))
    .catch(error => {
      catchError(error)
    })
}

const loadCarteira = (id) => {
  return new Promise((resolve, reject) => {
    vue.prototype.$api.query({
      query: gql` query($id: ID!){
        carteira(id: $id){
          id nome saldoCaixa saldoAcoes
        }
      }`,
      variables: {
        id
      }
    })
      .then(resp => resolve(resp.data.newAcao))
      .catch(error => reject(error))
  })
}

const saveCarteira = nome => {
  return new Promise((resolve, reject) => {
    vue.prototype.$api.mutate({
      mutation: gql`
         mutation($nome: String!) {
           saveCarteira(nome: $nome) {
             id
             nome
           }
         } `,
      variables: {
        nome
      }
    })
      .then(resp => resp.data.newAcao)
      .then(acao => store.commit('addCarteira', acao))
      .then(resp => {
        showToastSuccess(resp.nome + ' adicionada com sucesso!');
        resolve(resp)
      })
      .catch(error => {
        reject(false)
        catchError(error)
      })
  })
}

const setCarteira = (carteira) => {
  const dashboard = store.getters.dashboard
  const index = dashboard.carteiras.findIndex(i => i.id == carteira.id)
  const carteiras = dashboard.carteiras.splice(index, 1, carteira)
  dashboard.carteiras = carteiras
}

const setCarteiras = (carteiras) => {
  store.commit('carteiras', carteiras)
  setPatrimonio(carteiras)
}

const setPatrimonio = (carteiras) => {
  const calcTotalGeral = (carteiras) => carteiras.map(c => c.saldoCaixa + c.saldoAcoes).reduce((c, n) => c + n)
  let totalGeral = calcTotalGeral(carteiras)
  store.commit('patrimonio', totalGeral)
}
