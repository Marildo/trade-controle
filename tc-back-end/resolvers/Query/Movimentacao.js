const {MovimentacaoModel} = require('../../model')

const model = new MovimentacaoModel

const movimentacoes =(_) => {
    return model.findAll()
}

module.exports = {
    movimentacoes
}