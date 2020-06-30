const db = require('../config/db')
const dateUtils = require('../lib/dateUtils')

const table = () => db('historicos_carteiras')

const lastMonthGroupByData = () => {
  return new Promise((resolve, reject) => {
      table()
      .select(['historicos_carteiras.data_historico as dataHistorico',
      'historicos_carteiras.saldo_ativos as saldoAtivos',
      'historicos_carteiras.saldo_caixa as saldoCaixa',
      'carteiras.nome as title'])
      .innerJoin('carteiras', 'carteira_id', 'carteiras.id')
      .where('data_historico','>=',dateUtils.startOfMonth(new Date()))
      .then((resp) => resolve(resp))
      .catch((error) => {
        console.log(error)
        reject(error.detail)
      })
  })
}

module.exports = {
  lastMonthGroupByData,
}
