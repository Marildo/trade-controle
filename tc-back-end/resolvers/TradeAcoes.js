const { AcaoModel } = require('../model')

const dataCompra = (trade) => trade.data_compra

const dataVenda = (trade) => trade.data_venda

const precoCompra = (trade) => trade.preco_compra

const precoVenda = (trade) => trade.preco_venda

const acao = (trade) => new AcaoModel().findById(trade.acao_id)

module.exports = {
  dataCompra,
  dataVenda,
  precoCompra,
  precoVenda,
  acao
}