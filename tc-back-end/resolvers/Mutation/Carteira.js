const {carteiras, nextId} = require('../../data/db')

module.exports = {
    newCarteira(_, {nome}) {
        const carteria = {
            id: nextId,
            nome
        }

        carteiras.push(carteria)
        return carteria
    }
}