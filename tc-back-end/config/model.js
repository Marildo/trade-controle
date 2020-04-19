const db = require('./db')

const carteiraModel = () => db('carteiras')

module.exports = {
    carteiraModel
}
