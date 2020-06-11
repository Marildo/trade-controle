import vue from 'vue'
import { carteira, carteiras } from '../../graphql/carteiras'

const loadCarteiras = (context) => {
  vue.prototype.$apollo.query({
    query: carteiras
  })
    .then(resp => resp.data.carteiras)
    .then(carteiras => {
      context.commit('SET_CARTEIRAS', carteiras)
      context.dispatch('sumCarteiras', carteiras)
    })
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

const sumCarteiras = (context, carteiras) => {
  const sum = {
    saldoAcoes: carteiras.map(c => c.saldoAcoes).reduce((c, n) => c + n),
    saldoCaixa: carteiras.map(c => c.saldoCaixa).reduce((c, n) => c + n),
    resultadoMensal: carteiras.map(c => c.resultadoMensal).reduce((c, n) => c + n),
    resultadoSemanal: carteiras.map(c => c.resultadoSemanal).reduce((c, n) => c + n),
    ultimoResultado: carteiras.map(c => c.ultimoResultado).reduce((c, n) => c + n)
  }
  context.commit('SET_SUM', sum)
}

export {
  loadCarteiras,
  loadCarteira,
  sumCarteiras
}
