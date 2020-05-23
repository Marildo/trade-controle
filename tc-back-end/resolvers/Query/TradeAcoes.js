const {TradeAcaoModel} = require('../../model/')

const model = new TradeAcaoModel

function tradeAcoes(_) {
  return model.findAll()
}

module.exports = {
    tradeAcoes
}