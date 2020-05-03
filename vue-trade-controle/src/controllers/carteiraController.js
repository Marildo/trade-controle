import gql from 'graphql-tag'
import vue from 'vue'

function CarteiraController() {

  var carteiras

  this.findAll = () => {
    return new Promise((resolve, reject) => {
      vue.prototype.$api.query({
        query: gql`
          query{
            carteiras {
              id nome saldoCaixa
            }
          }`
      }).then(resp => {
        carteiras = resp.data.carteiras
        resolve(carteiras)
      }).catch(error => reject(error))
    })
  },

  this.findById = (id) => {
    return vue.prototype.$api.query({
      query: gql` query($id: ID!){
        carteira(id: $id){
          id nome saldoCaixa
        }
      }`,
      variables:{
        id
      }
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