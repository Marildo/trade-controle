const acaoModel = require('./acaoModel')
const carteiraModel = require('./carteiraModel')
const movimentacaoModel = require('./movimentacaoModel')
const setorModel = require('./setorModel')
const TradeAcaoModel = require('./tradeAcoesModel')
const SummaryAcoesModel = require('./summaryAcoesModel')

//TODO é possivel deixar isso mais generico? SIMMM!

module.exports = {
    acaoModel,
    setorModel,    
    carteiraModel,
    movimentacaoModel,
    TradeAcaoModel,
    SummaryAcoesModel
}
