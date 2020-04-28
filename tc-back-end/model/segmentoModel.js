const db = require('../config/db')

const table = () => db('segmentos')

function SegmentoModel() {

    this.findById = (id) => {
        return new Promise((resolve, reject) => {
            table()
                .where('id', id)
                .first()
                .then(resp => resolve(resp))
                .catch(error => {
                    console.log(error)
                    reject(error.sqlMessage)
                })
        })
    }

    this.save = (segmento) => {
        return new Promise((resolve, reject) => {
            this.findById(segmento.id)
                .then(resp => {
                    if (resp) {
                        resolve(resp)
                    } else {                    
                        table()
                            .insert(segmento)
                            .returning('*')
                            .then(resp => resolve(resp[0]))
                            .catch(error => {
                                console.log(error)
                                reject(error.detail)
                            })
                    }
                })
                .catch(error => {
                    console.log(error)
                    reject(error.detail)
                })
        })
    }
}

module.exports = SegmentoModel