import vue from 'vue'
import { carteira, carteiras } from '../../graphql/carteiras'
import { saveTradeAcao, movimentacoesByIdCarteira, deleteMovimentacao } from '../../graphql/lancamentos'

// TODO centralizar tratamentos de erros

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

const saveTrade = (context, trade) => {
  return new Promise((resolve, reject) => {
    vue.prototype.$apollo.mutate({
      mutation: saveTradeAcao,
      variables: {
        ...trade,
        quantidade: parseFloat(trade.quantidade),
        valor: parseFloat(trade.valor),
        corretagem: parseFloat(trade.corretagem),
        impostos: parseFloat(trade.impostos),
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
            context.dispatch('loadCarteiras', trade.carteira.id)
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
  sumCarteiras,

  saveTrade,
  loadLancamentos,
  deleteLancamento
}
