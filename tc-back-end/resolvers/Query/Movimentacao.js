const model = require('../../model/movimentacaoModel')

const movimentacoesByIdCarteira = (_, { idCarteira }) => {
  return model.findByIdCarteira(idCarteira)
}

module.exports = {
  movimentacoesByIdCarteira
}
