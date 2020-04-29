const Acao = require('./Acao')
const Carteira = require('./Carteira')
const Movimentacao = require('./Movimentacao')

module.exports = {
    helo() {
        return `Api rodando!  ${new Date}`
    },
    ...Acao,
    ...Carteira,
    ...Movimentacao
}