const Acao = require('./Acao')
const Carteira = require('./Carteira')
const Movimentacao = require('./Movimentacao')
const TipoLancamento = require('./TipoLancamento')
const TradeAcoes = require('./TradeAcoes')

module.exports = {
    helo() {
        return `Api rodando!  ${new Date}`
    },
    ...Acao,
    ...Carteira,
    ...Movimentacao,
    ...TipoLancamento,
    ...TradeAcoes
}