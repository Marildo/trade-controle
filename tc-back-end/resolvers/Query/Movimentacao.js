const { MovimentacaoModel } = require('../../model')

const model = new MovimentacaoModel

const movimentacoes = (_) => {
    return model.findAll()
}

const movimentacoesByIdCarteira = (_, { idCarteira }) => {
    return model.findByIdCarteira(idCarteira)
}


module.exports = {
    movimentacoes,
    movimentacoesByIdCarteira
}