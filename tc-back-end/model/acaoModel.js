const db = require('../config/db')

const baseModel = require('./baseModel')

const table = () => db('acoes')

const selectAcao = () => {
  return table()
    .select([
      'acoes.*',
      'setores.nome as setor',
      'subsetores.nome as subsetor',
      'segmentos.nome as segmento',
    ])
    .innerJoin('setores', 'setor_id', 'setores.id')
    .innerJoin('subsetores', 'subsetor_id', 'subsetores.id')
    .innerJoin('segmentos', 'segmento_id', 'segmentos.id')
}

const findById = (id) => baseModel.findById(table, id)

const save = (acao) => baseModel.save(table, acao)

const findAll = () => {
  return new Promise((resolve, reject) => {
    selectAcao()
      .then((resp) => resolve(resp))
      .catch((error) => {
        console.log(error)
        reject(error.detail)
      })
  })
}

const findByCodigo = (codigo) => {
  return new Promise((resolve, reject) => {
    selectAcao()
      .where('codigo', codigo.toUpperCase())
      .first()
      .then((resp) => resolve(resp))
      .catch((error) => {
        console.log(error)
        reject(error.detail)
      })
  })
}

const updatePrice = (id, price) => {
  if (isNaN(price)) {
    return
  }
  return new Promise((resolve, reject) => {
    table()
      .where('id', '=', id)
      .update({ preco: price })
      .then((resp) => resolve(resp))
      .catch((error) => reject(error))
  })
}

module.exports = {save, findById, findAll, findByCodigo, updatePrice }
