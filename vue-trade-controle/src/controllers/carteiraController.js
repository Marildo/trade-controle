import gql from 'graphql-tag'
import vue from 'vue'

function CarteiraController() {

    this.findAll = function () {
        return vue.prototype.$api.query({
            query: gql`{
              carteiras {
                id
                nome
              }
            }`
        })
    },

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