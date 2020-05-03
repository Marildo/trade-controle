const db = require('../config/db')
const { tiposLancamentos } = require('../model/enunsModel')

const table = () => db('carteiras')

function CarteiraModel() {

    this.findAll = () => {
        return new Promise((resolve, reject) => {
            table()
                .select()
                .then(resp => resolve(resp))
                .catch(error => {
                    console.log(error)
                    reject(error.detail)
                })
        })
    }

    this.findById = (id) => {
        return new Promise((resolve, reject) => {
            table()
                .select()
                .where('id', id)
                .first()
                .then(resp => resolve(resp))
                .catch(error => {
                    console.log(error)
                    reject(error.detail)
                })
        })
    }

    this.calculateSaldoCaixa = (id) => {
        return new Promise((resolve, reject) => {
            const allTipos = tiposLancamentos()
            const tiposSaida = allTipos.filter(t => t.isSaida).map(t => t.key)
            const tiposEntrada = allTipos.filter(t => !t.isSaida).map(t => t.key)

            const select =
                `SELECT COALESCE(
                 SUM(CASE WHEN tipo IN (${tiposEntrada}) THEN valor ELSE 0 END) -
                 SUM(CASE WHEN tipo IN (${tiposSaida}) THEN valor ELSE 0 END),
                 0) saldo FROM movimentacoes_carteiras
                 WHERE carteira_id = ?`

            db.raw(select, [id])
                .then(resp => resolve(resp.rows[0].saldo))
                .catch(error => {
                    console.log(error)
                    reject(error.detail)
                })
        })
    }

    this.save = ({ nome }) => {
        return new Promise((resolve, reject) => {
            const carteira = {
                nome
            }
            table()
                .insert(carteira)
                .returning('*')
                .then(resp => resolve(resp[0]))
                .catch(error => {
                    console.log(error)
                    reject(error.detail)
                })
        })
    }
}

module.exports = CarteiraModel