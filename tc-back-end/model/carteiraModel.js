const db = require('../config/db')

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