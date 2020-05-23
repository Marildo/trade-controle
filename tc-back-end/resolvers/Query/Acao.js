const { AcaoModel } = require('../../model/')

const model = new AcaoModel      

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