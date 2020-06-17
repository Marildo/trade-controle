import vue from 'vue'
import { carteira, carteiras } from '../../graphql/carteiras'
import { saveTradeAcao, movimentacoesByIdCarteira, deleteMovimentacao } from '../../graphql/lancamentos'
import { stringToFloat } from '../../utils/numberUtils'

// TODO centralizar tratamentos de erros

const loadCarteiras = (context) => {
  vue.prototype.$apollo.query({
    query: carteiras
  })
    .then(resp => resp.data.carteiras)
    .then(carteiras => {
      context.commit('SET_CARTEIRAS', carteiras)
      sumCarteiras(context, carteiras)
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
    .then(carteira => {
      context.commit('SET_CARTEIRA', carteira)
      updateCarteiras(context, carteira)
    })
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

const updateCarteiras = (context, carteira) => {
  const carteiras = context.state.carteiras
  if (carteiras === undefined || carteira.lenght === 0) {
    context.dispatch('loadCarteiras')
  } else {
    context.commit('UPDATE_CARTEIRAS', carteira)
    sumCarteiras(context, carteiras)
  }
}

const saveTrade = (context, trade) => {
  console.info(trade.precoCompra)

  trade.precoCompra = stringToFloat(trade.precoCompra)
  trade.precoVenda = stringToFloat(trade.precoVenda)

  console.info(trade.precoCompra)

  const split = trade.dataTrade.split('/')

  if (trade.precoCompra > 0) {
    trade.dataCompra = new Date(split[1] + '/' + split[0] + '/' + split[2])
  }

  if (trade.precoVenda > 0) {
    trade.dataVenda = new Date(split[1] + '/' + split[0] + '/' + split[2])
  }

  return new Promise((resolve, reject) => {
    vue.prototype.$apollo.mutate({
      mutation: saveTradeAcao,
      variables: {
        ...trade,
        quantidade: parseInt(trade.quantidade),
        corretagem: stringToFloat(trade.corretagem),
        impostos: stringToFloat(trade.impostos),
        idCarteira: trade.carteira.id,
        acao: {
          id: trade.acao.id,
          codigo: trade.acao.codigo
        }
      }
    })
      .then(resp => resp.data.saveTradeAcao)
      .then(resp => {
        // TODO não recarregar tudo
        vue.prototype.$apollo.resetStore()
          .then(r => {
            context.dispatch('loadCarteira', trade.carteira.id)
            context.commit('ADD_LANCAMENTO', resp)
          })

        resolve(resp)
      })
      .catch(erro => {
        console.log(erro)
        console.log(erro.networkError.result.errors[0])
        reject(erro.networkError.result.errors[0].message)
      })
  })
}

const loadLancamentos = (context, idCarteira) => {
  vue.prototype.$apollo.query({
    query: movimentacoesByIdCarteira,
    variables: { idCarteira: parseInt(idCarteira) }
  })
    .then(resp => resp.data.movimentacoesByIdCarteira)
    .then(lancamentos => context.commit('SET_LANCAMENTOS', lancamentos))
    .catch(error => console.log(error))
}

const deleteLancamento = (context, lancamento) => {
  vue.prototype.$apollo.mutate({
    mutation: deleteMovimentacao,
    variables: { id: lancamento.id }
  })
    .then(resp => {
      context.commit('REMOVE_LANCAMENTO', lancamento)
      context.dispatch('loadCarteira', lancamento.idCarteira)
    })
    .catch(error => {
      console.log(error)
      console.log(error.networkError)
    })
}

export {
  loadCarteiras,
  loadCarteira,

  saveTrade,
  loadLancamentos,
  deleteLancamento
}
