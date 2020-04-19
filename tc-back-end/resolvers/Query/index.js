const Acao = require('./Acao')
const Carteira = require('./Carteira')

module.exports = {
    helo() {
        return `Api rodando!  ${new Date}`
    },
    ...Acao,
    ...Carteira
}