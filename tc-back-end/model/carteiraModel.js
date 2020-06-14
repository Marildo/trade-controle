const db = require('../config/db')
const { tiposLancamentos } = require('../model/enunsModel')
const { save, findById, findAll } = require('./baseModel')

const table = () => db('carteiras')

function CarteiraModel() {

    this.findAll = () => findAll(table)

    this.findById = (id) => findById(table, id)
    
    this.save = (carteira) => save(table, carteira)

    this.calculateSaldoCaixa = (id) => {
        return new Promise((resolve, reject) => {
            const allTipos = tiposLancamentos()
            const tiposSaida = allTipos.filter(t => t.isSaida).map(t => t.key)
            const tiposEntrada = allTipos.filter(t => !t.isSaida).map(t => t.key)

            const select =
                `SELECT COALESCE(
                    SUM(CASE WHEN tipo IN (${tiposSaida}) THEN valor ELSE 0 END) -
                    SUM(CASE WHEN tipo IN (${tiposEntrada}) THEN valor ELSE 0 END), 0) saldo 
                 FROM movimentacoes_carteiras
                 WHERE carteira_id = ?`
            db.raw(select, [id])
                .then(resp => resolve(resp.rows[0].saldo))
                .catch(error => {
                    console.log(error)
                    reject(error.detail)
                })
        })
    }

    this.calculateSaldoAcoes = (id) => {
        return new Promise((resolve, reject) => {
            const select =
               `SELECT COALESCE(SUM(quantidade * a.preco),0) AS total
                FROM summary_acoes 
                INNER JOIN acoes a ON acao_id = a.id
                WHERE carteira_id = ?`
            db.raw(select, [id])
                .then(resp => resolve(resp.rows[0].total))
                .catch(error => {
                    console.log(error)
                    reject(error.detail)
                })
        })
    }
}

module.exports = CarteiraModel