import gql from 'graphql-tag'
import vue from 'vue'

import store from '@/store';
import { showToastSuccess, catchError } from '@/lib/messages'

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
    .then(carteiras => store.dispatch('carteiras', carteiras))
    .catch(error => catchError(error))
}

const loadCarteira = (id) => {
  vue.prototype.$api.resetStore()
    .then(() => {
      vue.prototype.$api.query({
        query: gql` query($id: ID!){
        carteira(id: $id){
          id nome saldoCaixa saldoAcoes
          portifolio{     
            quantidade  precoMedio totalAtual custoTotal 
            resultado percentual  idAcao codigoAcao cotacao
            idSetor idSubsetor idSegmento
          }
        }
      }`,
        variables: {
          id
        }
      })
        .then(resp => resp.data.carteira)
        .then(carteira => store.dispatch('updateCarteira', carteira))
        .catch(error => catchError(error))
    })
    .catch(error => catchError(error))
}

// TODO missing param for named route "Carteira": Expected "id" to be defined quando adicona uma nova carteira
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
      .then(resp => resp.data.saveCarteira)
      .then(carteira => {
        showToastSuccess(carteira.nome + ' adicionada com sucesso!')
        store.dispatch('addCarteira', carteira)
      })
      .then(resolve(true))
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


export {
  loadCarteiras,
  loadCarteira,
  saveCarteira,
  setCarteira
}
