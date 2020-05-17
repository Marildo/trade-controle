const db = require('../config/db')
const {save,findAll,findById, deleteById} = require('./baseModel')

const table = () => db('movimentacoes_carteiras')

function MovimentacaoModel() {
    this.findAll = () => findAll(table)

    this.findById = (id) => findById(table,id)

    this.save = (movimentacao) =>  save(table,movimentacao)
    
    this.deleteById = (id) => deleteById(table,id)

    //TODO criar metodo no base model que receba o where
    this.findByIdCarteira = (idCarteira) => {
        return new Promise((resolve, reject) => {
            table()
                .where('carteira_id',idCarteira)
                .then(resp => resolve(resp))
                .catch(error => reject(error.detail))
        })
    }

}

module.exports = MovimentacaoModel