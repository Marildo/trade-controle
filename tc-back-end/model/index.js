const acaoModel = require('./acaoModel')
const carteiraModel = require('./carteiraModel')
const movimentacaoModel = require('./movimentacaoModel')
const setorModel = require('./setorModel')
const tradeAcaoModel = require('./tradeAcoesModel')
const summaryAcoesModel = require('./summaryAcoesModel')

//TODO é possivel deixar isso mais generico? SIMMM!

module.exports = {
    acaoModel,
    setorModel,    
    carteiraModel,
    movimentacaoModel,
    tradeAcaoModel,
    summaryAcoesModel
}
