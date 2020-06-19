const db = require('../config/db')
const { save, findAll, update } = require('./baseModel')
const { assertObjectType } = require('graphql')

const table = () => db('trade_acoes')

function TradeAcaoModel() {
  this.save = async (trade) => {
    if (trade.finalizada) {
      delete trade.compra
      delete trade.venda
      save(table, trade)
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
          await save(table, trade)
        } else {
          let quantidadeAFinalizar = trade.quantidade
          tradesAbertos.forEach(async (tradeAberto) => {
            if (quantidadeAFinalizar > 0) {
              quantidadeAFinalizar = await finalizeTrade(
                trade,
                tradeAberto,
                quantidadeAFinalizar
              )
            }
          })
        }
      } catch (error) {
        console.log(error)
      }
    }
  }

  finalizeTrade = async (trade, tradeAberto, quantidadeAFinalizar) => {
    const valor = trade.compra ? 'preco_compra' : 'preco_venda'
    const data = trade.compra ? 'data_compra' : 'data_venda'

    if (tradeAberto.quantidade > quantidadeAFinalizar) {
      const copyTrade = {
        ...tradeAberto,
        id: undefined,
        finalizada: true,
        quantidade: quantidadeAFinalizar,
      }

      copyTrade[valor] = trade[valor]
      copyTrade[data] = trade[data]
      await save(table, copyTrade).catch((error) => console.log(error))

      tradeAberto.quantidade -= quantidadeAFinalizar
      await update(table, tradeAberto).catch((error) => console.log(error))

      return 0
    } else if (tradeAberto.quantidade < quantidadeAFinalizar) {
      tradeAberto[valor] = trade[valor]
      tradeAberto[data] = trade[data]
      tradeAberto.finalizada = true
      tradeAberto.corretagem = trade.corretagem
      tradeAberto.impostos = trade.impostos
      await update(table, tradeAberto)

      return quantidadeAFinalizar - tradeAberto.quantidade
    } else if (tradeAberto.quantidade === quantidadeAFinalizar) {
      update(table, tradeAberto)
      return 0
    }
  }

  this.findAll = () => findAll(table)

  this.findByMovimentacaoId = async (idMov) => {
    const trade = await table().select().where('movimentacao_id', idMov)
    if (trade.length > 0) {
      return {
        acao: { id: trade[0].acao_id },
        idCarteira: trade[0].carteira_id,
      }
    }
    return undefined
  }

  this.findByIdCarteiraIdAndIdAcao = (idCarteira, idAcao) => {
    const trade = table()
      .select()
      .where('carteira_id', idCarteira)
      .andWhere('acao_id', idAcao)
    return trade
  }
}

module.exports = TradeAcaoModel
