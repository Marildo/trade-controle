const { CarteiraModel } = require('../model/')

function acoes(){
    return []
}

function saldoCaixa(carteira){
    const carteiraModel = new CarteiraModel
    return carteiraModel.calculateSaldoCaixa(carteira.id)
}

function saldoAcoes(carteira){
    return  0.0
}


module.exports = {
    acoes,
    saldoCaixa,
    saldoAcoes
}