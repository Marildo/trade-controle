import vue from 'vue'
import { carteira, carteiras } from '../../graphql/carteiras'

const loadCarteiras = (context) => {
  vue.prototype.$apollo.query({
    query: carteiras
  })
    .then(resp => resp.data.carteiras)
    .then(carteiras => context.commit('SET_CARTEIRAS', carteiras))
    .catch(error => console.log(error))
}

const loadCarteira = (context, id) => {
  vue.prototype.$apollo.query({
    query: carteira,
    variables: {
      id
    }
  })
    .then(resp => resp.data.carteira)
    .then(carteira => context.commit('SET_CARTEIRA', carteira))
    .catch(error => console.log(error))
}

export {
  loadCarteiras,
  loadCarteira
}
