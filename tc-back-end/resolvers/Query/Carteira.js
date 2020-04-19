const {carteiras} = require('../../data/db')

module.exports = {
    carteira(_, args) {
        const selected = carteiras.filter(a => a.id == args.id)
        return selected ? selected[0] : null
    },
    carteiras() {
        return carteiras
    },
}