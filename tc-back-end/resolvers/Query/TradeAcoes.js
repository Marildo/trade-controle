const { tradeAcaoModel } = require("../../model")

const model = require('../../model/tradeAcoesModel')

function tradeAcoes(_) {
  return model.findAll()
}

module.exports = {
    tradeAcoes
}