const db = require('../config/db')

const table = () => db('movimentacoes_carteiras')

function MovimentacaoModel() {
    this.findAll = () => {
        return new Promise((resolve, reject) => {
            table()
                .then(resp => resolve(resp))
                .catch(error => reject(error.detail))
        })
    }

    this.save = (movimentacao) => {
        return new Promise((resolve, reject) => {
            table()
                .insert(movimentacao)
                .returning('*')
                .then(resp => resolve(resp[0]))
                .catch(error => reject(error.detail))
        })
    }
}

module.exports = MovimentacaoModel