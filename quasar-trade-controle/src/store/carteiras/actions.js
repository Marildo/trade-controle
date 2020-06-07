import gql from 'graphql-tag'
import vue from 'vue'

const loadCarteiras = (context) => {
  vue.prototype.$apollo.query({
    query: gql`
             query{
               carteiras {
                id nome saldoCaixa saldoAcoes
               }
            }`
  })
    .then(resp => resp.data.carteiras)
    .then(carteiras => context.commit('SET_CARTEIRAS', carteiras))
    .catch(error => console.log(error))
}

export {
  loadCarteiras
}
