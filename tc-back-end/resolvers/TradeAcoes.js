const { AcaoModel } = require('../model')

const dataTrade = (trade) => trade.data_trade

const acao = (trade) => new AcaoModel().findById(trade.acao_id)

module.exports = {
  dataTrade,
  acao
}