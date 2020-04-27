const db = require('../config/db')

function CarteiraModel() {

    table = () => db('carteiras')

    this.findAll = () => {
        return new Promise((resolve, reject) => {
            select()
                .then(resp => resolve(resp))
                .catch(error => {
                    console.log(error)
                    reject(error.detail)
                })
        })
    }

    this.save = (nome) => {
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