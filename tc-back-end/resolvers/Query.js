const {carteiras, acoes} = require('../data/db')

module.exports = {
        helo() {
            return `Api rodando!  ${new Date}`
        },
        carteira(_, args) {
            const selected = carteiras.filter(a => a.id == args.id)
            return selected ? selected[0] : null
        },
        carteiras() {
            return carteiras
        },
        acao(_, args) {
            const selected = acoes.filter(a => a.id == args.id)
            return selected ? selected[0] : null
        },
        acoes() {
            return acoes
        }
}