const historicoModel  = require('../../model/HistoricoModel')

const historicoLastMonthGroupByData = async (_) => {
  return historicoModel.lastMonthGroupByData()
}

module.exports = {
 historicoLastMonthGroupByData
}