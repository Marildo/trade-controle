const db = require('../config/db')
const { save, findAll } = require('./baseModel')

const table = () => db('trade_acoes')

function TradeAcaoModel() {
    this.save = (trade) => save(table, trade)
    this.findAll = () => findAll(table)
}



module.exports = TradeAcaoModel