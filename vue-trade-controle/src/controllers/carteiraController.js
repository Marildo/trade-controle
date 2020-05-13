import gql from 'graphql-tag'
import vue from 'vue'
import store from './../store/';

function CarteiraController() {

  this.loadCarteiras = () => {
    vue.prototype.$api.query({
      query: gql`
          query{
            carteiras {
              id nome saldoCaixa saldoAcoes
            }
          }`
    })
      .then(resp => store.dispatch('setCarteiras', resp.data.carteiras))
      .catch(error => {
        console.log(error)
        console.log(error.networkError.result.errors)
      })
  }


  this.loadCarteira  = (id) => {
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
    .then(resp =>{ 
      store.dispatch("updateCarteira", resp.data.carteira)
    })
    .catch(error => {
      console.log(error)
      console.log(error.networkError.result.errors[0].message );
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