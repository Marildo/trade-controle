const { CarteiraModel } = require('../model/')

function acoes(){
    return []
}

function saldoCaixa(carteira){
    const carteiraModel = new CarteiraModel
    return carteiraModel.calculateSaldoCaixa(carteira.id)
}

function saldoAcoes(carteira){
    const carteiraModel = new CarteiraModel
    return carteiraModel.calculateSaldoAcoes(carteira.id)
}

module.exports = {
    acoes,
    saldoCaixa,
    saldoAcoes
}