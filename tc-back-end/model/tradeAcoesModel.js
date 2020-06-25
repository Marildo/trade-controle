const db = require('../config/db')
const baseModel = require('./baseModel')

const table = () => db('trade_acoes')

const save = (trade) => {
  return new Promise(async (resolve, reject) => {
    if (trade.finalizada) {
      delete trade.compra
      delete trade.venda
      baseModel.save(table, trade)
    } else {
      try {
        const tradesAbertos = await table()
          .select()
          .where('carteira_id', trade.carteira_id)
          .andWhere('acao_id', trade.acao_id)
          .andWhere('finalizada', false)
          .andWhere(trade.compra ? 'preco_venda' : 'preco_compra', '>', 0)
          .orderBy(trade.compra ? 'data_venda' : 'data_compra')

        if (tradesAbertos.length === 0) {
          delete trade.compra
          delete trade.venda
          trade = await baseModel.save(table, trade)
        } else {
          let quantidadeAFinalizar = trade.quantidade

          let i = 0
          while (quantidadeAFinalizar > 0) {
            tradeAberto = tradesAbertos[i]
            i++
            if (tradeAberto.quantidade == quantidadeAFinalizar) {
              quantidadeAFinalizar = await finalizeWhenEqual(tradeAberto)
            } else {
              quantidadeAFinalizar = await finalizeTrade(
                trade,
                tradeAberto,
                quantidadeAFinalizar
              )
            }
          }
        }
        resolve(true)
      } catch (error) {
        console.log(error)
        reject(error)
      }
    }
  })
}

finalizeWhenEqual = async (trade) => {
  trade.finalizada = true
  await baseModel.update(table, trade)
  return 0
}

finalizeTrade = async (trade, tradeAberto, quantidadeAFinalizar) => {
  try {
    const valor = trade.compra ? 'preco_compra' : 'preco_venda'
    const data = trade.compra ? 'data_compra' : 'data_venda'

    if (tradeAberto.quantidade > quantidadeAFinalizar) {
      const copyTrade = {
        ...tradeAberto,
        id: undefined,
        finalizada: true,
        quantidade: tradeAberto.quantidade - quantidadeAFinalizar,
      }
      copyTrade[valor] = trade[valor]
      copyTrade[data] = trade[data]

      tradeAberto.quantidade -= quantidadeAFinalizar
      await baseModel.update(table, tradeAberto)
      await baseModel.save(table, copyTrade)

      return 0
    } else if (tradeAberto.quantidade < quantidadeAFinalizar) {
      tradeAberto[valor] = trade[valor]
      tradeAberto[data] = trade[data]
      tradeAberto.finalizada = true
      tradeAberto.corretagem = trade.corretagem
      tradeAberto.impostos = trade.impostos
      await baseModel.update(table, tradeAberto)

      return quantidadeAFinalizar - tradeAberto.quantidade
    }
  } catch (error) {
    console.log(error)
  }
}

const findAll = () => findAll(table)

const findByMovimentacaoId = async (idMov) => {
  const trade = await table().select().where('movimentacao_id', '=', idMov)
  if (trade.length > 0) {
    return {
      acao: { id: trade[0].acao_id },
      idCarteira: trade[0].carteira_id,
    }
  }
  return undefined
}

/*
const findByIdCarteiraIdAndIdAcao = (idCarteira, idAcao) => {
  const trade = table()
    .select()
    .where('carteira_id', idCarteira)
    .andWhere('acao_id', idAcao)
  return trade
}
*/

module.exports = { save, findByMovimentacaoId }
