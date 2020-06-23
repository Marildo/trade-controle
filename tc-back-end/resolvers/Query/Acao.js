const model  = require('../../model/acaoModel')

const acao = (_, {codigo}) => {      
    return model.findByCodigo(codigo)
}

const acoes = async (_) => {  
    return model.findAll()
}

module.exports = {
    acao,
    acoes,
}