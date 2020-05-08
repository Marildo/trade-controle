const Carteira = require('./Carteira')
const Acao = require('./Acao')
const Movimentacao = require('./Movimentacao')
const TradeAcoes = require('./TradeAcoes')

module.exports = {
    ...Carteira,
    ...Acao,
    ...Movimentacao,
    ...TradeAcoes,
}
