const Carteira = require('./Carteira')
const Acao = require('./Acao')
const Movimentacao = require('./Movimentacao')

module.exports = {
    ...Carteira,
    ...Acao,
    ...Movimentacao
}
