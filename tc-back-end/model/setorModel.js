const db = require('../config/db')

function SetorModel() {

    table = () => db('setores')

    this.findById = (id) => {
        return new Promise((resolve, reject) => {
            table()
                .where('id', id)
                .first()
                .then(resp => resolve(resp))
                .catch(error => reject(error.detail))
        })
    }

    this.save = (setor) => {
        return new Promise((resolve, reject) => {
            this.findById(setor.id)
                .then(resp => {
                    if (resp) {
                        resolve(resp)
                    } else {
                        table()
                            .insert(setor)
                            .returning('*')
                            .then(resp => resolve(resp[0]))
                            .catch(error => reject(error.detail))
                    }
                })
                .catch(error => reject(error.detail))
        })
    }
}

module.exports = SetorModel