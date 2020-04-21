const { acaoModel } = require('../../model')

// TODO renomear metodos e passar consulta para model

const acao = (_, args) => {
    return acaoModel()
        .select(['acoes.*',
            'setores.nome as setor',
            'subsetores.nome as subsetor',
            'segmentos.nome as segmento'])
        .innerJoin('setores', 'setor_id', 'setores.id')
        .innerJoin('subsetores', 'subsetor_id', 'subsetores.id')
        .innerJoin('segmentos', 'segmento_id', 'segmentos.id')
        .where('codigo', args.codigo.toUpperCase())
        .first()
        .catch((e) => console.log(e))
}

const acoes = (_) => {
    return acaoModel()
        .select(['acoes.*',
            'setores.nome as setor',
            'subsetores.nome as subsetor',
            'segmentos.nome as segmento'])
        .innerJoin('setores', 'setor_id', 'setores.id')
        .innerJoin('subsetores', 'subsetor_id', 'subsetores.id')
        .innerJoin('segmentos', 'segmento_id', 'segmentos.id')
}

module.exports = {
    acao,
    acoes,
}