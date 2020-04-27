const AcModel = require('../../model/acaoModel')
const model = new AcModel      

const acao = (_, {codigo}) => {      
    return model.findByCodigo(codigo)
}

const acoes = (_) => {     
    return model.findAll()
}

module.exports = {
    acao,
    acoes,
}