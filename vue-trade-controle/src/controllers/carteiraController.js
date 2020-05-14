import gql from 'graphql-tag'
import vue from 'vue'
 

import { setCarteira } from './mainController'

function CarteiraController() {

  this.loadCarteiras = () => {
    return vue.prototype.$api.query({
      query: gql`
          query{
            carteiras {
              id nome saldoCaixa saldoAcoes
            }
          }`
    })
  }

  this.loadCarteira = (id) => {
    return vue.prototype.$api.query({
      query: gql` query($id: ID!){
        carteira(id: $id){
          id nome saldoCaixa saldoAcoes
        }
      }`,
      variables: {
        id
      }
    })
      .then(resp => {
        setCarteira(resp.data.carteira)
        // store.dispatch("updateCarteira", resp.data.carteira)
      })
      .catch(error => {
        console.log(error)
        console.log(error.networkError.result.errors[0].message);
      })
  }

  this.save = nome => {
    return vue.prototype.$api.mutate({
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
  }

}

export default CarteiraController