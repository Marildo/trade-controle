const db = require('../config/db')
const {findById} = require('./baseModel')

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

    this.findById = (id) => findById(table,id)

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

    this.save = (acao) => {
        return new Promise((resolve, reject) => {          
            table()
                .insert(acao)
                .returning('*')
                .then(resp => resolve(resp[0]))
                .catch(error => {
                    console.log(error)
                    reject(error.detail)
                })
        })
    }
}

module.exports = AcaoModel