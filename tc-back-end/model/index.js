const AcaoModel = require('./acaoModel')
const carteiraModel = require('./carteiraModel')
const movimentacaoModel = require('./movimentacaoModel')

const SetorModel = require('./setorModel')
const SubsetorModel = require('./subSetorModel')
const SegmentoModel = require('./segmentoModel')
const TradeAcaoModel = require('./tradeAcoesModel')
const SummaryAcoesModel = require('./summaryAcoesModel')

//TODO é possivel deixar isso mais generico? SIMMM!

module.exports = {
    AcaoModel,
    carteiraModel,
    movimentacaoModel,
    TradeAcaoModel,
    SummaryAcoesModel,
    
    SetorModel,
    SubsetorModel,
    SegmentoModel
}
