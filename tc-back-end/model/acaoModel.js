const db = require('../config/db')

function AcaoModel() {

    table = () => db('acoes')

    selectAcao = () => {
        return table()
            .selectAcao(['acoes.*',
                'setores.nome as setor',
                'subsetores.nome as subsetor',
                'segmentos.nome as segmento'])
            .innerJoin('setores', 'setor_id', 'setores.id')
            .innerJoin('subsetores', 'subsetor_id', 'subsetores.id')
            .innerJoin('segmentos', 'segmento_id', 'segmentos.id')
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