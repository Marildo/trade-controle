const db = require('../config/db')
const baseModel = require('./baseModel')

const table = () => db('movimentacoes_carteiras')

const findById = (id) => baseModel.findById(table, id)

const save = (movimentacao) => baseModel.save(table, movimentacao)

const deleteById = (id) => baseModel.deleteById(table, id)

//TODO criar metodo no base model que receba o where
const findByIdCarteira = (idCarteira) => {
  return new Promise((resolve, reject) => {
    table()
      .where('carteira_id', idCarteira)
      .then((resp) => resolve(resp))
      .catch((error) => reject(error.detail))
  })
}

module.exports = {
   findById, 
   save, 
   deleteById, 
   findByIdCarteira
}
