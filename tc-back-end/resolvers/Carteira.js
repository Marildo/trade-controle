const { CarteiraModel } = require('../model/')

function acoes(){
    return []
}

function saldoCaixa(carteira){
    const carteiraModel = new CarteiraModel
    return carteiraModel.calculateSaldoCaixa(carteira.id)
}

module.exports = {
    acoes,
    saldoCaixa
}