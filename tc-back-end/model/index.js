const db = require('../config/db')

const carteiraModel = () => db('carteiras')
const acaoModel = () => db('acoes')


module.exports = {
    acaoModel,
    carteiraModel
}
