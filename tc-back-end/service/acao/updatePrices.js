const schedule = require('node-schedule')

const model = require('../../model/acaoModel')
const { updateCarteiras } = require('../../model/carteiraModel')

const { findCotacao } = require('./statusInvest')

const updatePrices = () => {
  update()
  const rule = new schedule.RecurrenceRule()
  //TODO remover em producao
  // rule.dayOfWeek = new schedule. Range(1,5)
  // rule.hour = new schedule.Range(8, 18)
  rule.second = 30 // new schedule.Range(1,59)
  schedule.scheduleJob(rule, update)
}

const update = () => {
  model
    .findAll()
    .then((acoes) => {
      acoes.forEach((acao) => {
        findCotacao(acao.codigo)
          .then((price) => parseFloat(price))
          .then((price) =>
            model
              .updatePrice(acao.id, price)
              .then(console.log('Updated ', acao.codigo))
              .catch((error) => console.log(error))
          )
          .catch((error) => console.log(error))
      })
    })
    .then(() => {
      console.log('upCarteiras')
      updateCarteiras()
    })
    .catch((error) => console.log(error))
}

module.exports = {
  updatePrices,
}
