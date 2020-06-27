import vue from 'vue'
import { carteira, carteiras, saveCarteira } from '../../graphql/carteiras'
import { saveTradeAcao, movimentacoesByIdCarteira, deleteMovimentacao, saveMovimentacao } from '../../graphql/lancamentos'
import { stringToFloat } from '../../utils/numberUtils'

// TODO centralizar tratamentos de erros

// TODO serar actions de trades e carteiras em arquivos diferentes

const loadCarteiras = (context) => {
  vue.prototype.$apollo
    .query({
      query: carteiras
    })
    .then((resp) => resp.data.carteiras)
    .then((carteiras) => {
      context.commit('SET_CARTEIRAS', carteiras)
      sumCarteiras(context, carteiras)
    })
    .catch((error) => console.log(error))
}

const loadCarteira = (context, id) => {
  vue.prototype.$apollo
    .query({
      query: carteira,
      variables: { id },
      fetchPolicy: 'network-only'
    })
    .then((resp) => resp.data.carteira)
    .then((carteira) => {
      context.commit('SET_CARTEIRA', carteira)
      updateCarteiras(context, carteira)
    })
    .catch((error) => console.log(error))
}

const sumCarteiras = (context, carteiras) => {
  const sum = {
    saldoAtivos: carteiras.map((c) => c.saldoAtivos).reduce((c, n) => c + n),
    saldoCaixa: carteiras.map((c) => c.saldoCaixa).reduce((c, n) => c + n),
    resultadoMensal: carteiras.map((c) => c.resultadoMensal).reduce((c, n) => c + n),
    resultadoSemanal: carteiras.map((c) => c.resultadoSemanal).reduce((c, n) => c + n),
    ultimoResultado: carteiras.map((c) => c.ultimoResultado).reduce((c, n) => c + n)
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

const addCarteira = (context, nome) => {
  return new Promise((resolve, reject) => {
    vue.prototype.$apollo.mutate({
      mutation: saveCarteira,
      variables: { nome }
    })
      .then(() => vue.prototype.$apollo.resetStore())
      .then(() => context.dispatch('loadCarteiras'))
      .then(() => resolve(true))
      .catch(error => {
        if (error.networkError.result.errors) {
          console.log(error.networkError.result.errors[0].message)
        }
        if (error.networkError) {
          console.log(error.networkError)
        }
        console.log(error)
        reject(error.networkError.result.errors[0].message)
      })
  })
}

const saveTrade = (context, trade) => {
  return new Promise((resolve, reject) => {
    const precoCompra = stringToFloat(trade.precoCompra)
    const precoVenda = stringToFloat(trade.precoVenda)

    const split = trade.dataTrade.split('/')

    let dataCompra
    if (precoCompra > 0) {
      dataCompra = new Date(split[1] + '/' + split[0] + '/' + split[2])
    }

    let dataVenda
    if (precoVenda > 0) {
      dataVenda = new Date(split[1] + '/' + split[0] + '/' + split[2])
    }
    vue.prototype.$apollo
      .mutate({
        mutation: saveTradeAcao,
        variables: {
          dataCompra,
          dataVenda,
          precoCompra,
          precoVenda,
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
      .then((resp) => resp.data.saveTradeAcao)
      .then((resp) => {
        // TODO não recarregar tudo
        // vue.prototype.$apollo.resetStore().then(() => {
        context.dispatch('loadCarteira', trade.carteira.id)
        context.commit('ADD_LANCAMENTO', resp)
        resolve(resp)
      //  })
      })
      .catch((erro) => {
        console.log(erro)
        console.log(erro.networkError.result.errors[0])
        reject(erro.networkError.result.errors[0].message)
      })
  })
}

const loadLancamentos = (context, idCarteira) => {
  vue.prototype.$apollo
    .query({
      query: movimentacoesByIdCarteira,
      variables: { idCarteira: parseInt(idCarteira) }
    })
    .then((resp) => resp.data.movimentacoesByIdCarteira)
    .then((lancamentos) => context.commit('SET_LANCAMENTOS', lancamentos))
    .catch((error) => console.log(error))
}

const addLancamento = (context, lancamento) => {
  return new Promise((resolve, reject) => {
    const idCarteira = parseInt(lancamento.carteira.id)
    const valor = stringToFloat(lancamento.valor)

    const split = lancamento.dataMovimentacao.split('/')
    const dataMovimentacao = new Date(split[1] + '/' + split[0] + '/' + split[2])

    vue.prototype.$apollo.mutate({
      mutation: saveMovimentacao,
      variables: {
        tipo: lancamento.tipo.key,
        descricao: lancamento.descricao,
        valor,
        idCarteira,
        dataMovimentacao
      }
    })
      .then(() => {
      //  vue.prototype.$apollo.resetStore().then(() => {
        context.dispatch('loadCarteira', idCarteira)
        context.dispatch('loadLancamentos', idCarteira)
        resolve(true)
        // })
      })
      .catch(error => {
        console.log(error)
        if (error.networkError.result.errors) {
          console.log(error.networkError.result.errors[0].message)
        }
        if (error.networkError) {
          console.log(error.networkError)
        }
        reject(error.networkError.result.errors[0].message)
      })
  })
}

const deleteLancamento = (context, lancamento) => {
  vue.prototype.$apollo
    .mutate({
      mutation: deleteMovimentacao,
      variables: { id: lancamento.id }
    })
    .then(() => {
      vue.prototype.$apollo.resetStore().then(() => {
        context.commit('REMOVE_LANCAMENTO', lancamento)
        context.dispatch('loadCarteira', lancamento.idCarteira)
      })
    })
    .catch((error) => {
      console.log(error)
      console.log(error.networkError)
    })
}

export {
  loadCarteiras,
  loadCarteira,
  addCarteira,
  saveTrade,
  loadLancamentos,
  addLancamento,
  deleteLancamento
}
