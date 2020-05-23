const db = require('../config/db')
const { findById, findAll, save } = require('./baseModel')

const table = () => db('acoes')

const selectAcao = () => {
    return table()
        .select(['acoes.*',
            'setores.nome as setor',
            'subsetores.nome as subsetor',
            'segmentos.nome as segmento'])
        .innerJoin('setores', 'setor_id', 'setores.id')
        .innerJoin('subsetores', 'subsetor_id', 'subsetores.id')
        .innerJoin('segmentos', 'segmento_id', 'segmentos.id')
}

function AcaoModel() {
    this.findById = (id) => findById(table, id)

    this.save = (acao) => save(table, acao)

    this.findAll = () => {
        return new Promise((resolve, reject) => {
            selectAcao()
                .then(resp => resolve(resp))
                .catch(error => {
                    console.log(error)
                    reject(error.detail)
                })
        })
    }

    this.findByCodigo = (codigo) => {
        return new Promise((resolve, reject) => {
            selectAcao()
                .where('codigo', codigo.toUpperCase())
                .first()
                .then(resp => resolve(resp))
                .catch(error => {
                    console.log(error)
                    reject(error.detail)
                })
        })
    }

    this.updatePrice = (id, price) => {
        return new Promise((resolve, reject) => {
            table()
                .where('id', '=', id)
                .update({ preco: price })
                .then(resp => resolve(resp))
                .catch(error => reject(error))
        })
    }
}

module.exports = AcaoModel