const db = require('../config/db')

const table = () => db('subsetores')

function SubsetorModel() {

    this.findById = (id) => {
        return new Promise((resolve, reject) => {
            table()
                .where('id', id)
                .first()
                .then(resp => resolve(resp))
                .catch(error => {
                    console.log(error)
                    reject(error.detail)
                })
        })
    }

    this.save = (subsetor) => {
        return new Promise((resolve, reject) => {
            this.findById(subsetor.id)
                .then(resp => {
                    if (resp) {
                        resolve(resp)
                    } else {                    
                        table()
                            .insert(subsetor)
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

module.exports = SubsetorModel