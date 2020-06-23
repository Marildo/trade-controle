const db = require('../config/db')
const baseModel = require('./baseModel')

const saveSetor = (setor) => save('setores', setor)

const saveSubSetor = (subsetor) => save('subsetores', subsetor)

const saveSegmento = (segmento) => save('segmentos', segmento)

const save = (tableName, item) => {
  return new Promise((resolve, reject) => {

    const table = () => db(tableName)

    baseModel.findById(table, item.id)
      .then((resp) => {
        if (resp) {
          resolve(resp)
        } else {
            table()
            .insert(item)
            .returning('*')
            .then((resp) => resolve(resp[0]))
            .catch((error) => reject(error))
        }
      })
      .catch((error) => reject(error))
  })
}

module.exports = { saveSetor, saveSubSetor, saveSegmento }
