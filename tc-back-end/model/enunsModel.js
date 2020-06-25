function tipoLancamentoFactory(key, descricao, isSaida) {
    return {
        key,
        descricao,
        isSaida
    }
}

const tiposLancamentos = () => [
    tipoLancamentoFactory(0, 'Compra', true),
    tipoLancamentoFactory(1, 'Venda', false),
    tipoLancamentoFactory(2, 'Aporte', false),
    tipoLancamentoFactory(3, 'Retirada', true),
    tipoLancamentoFactory(4, 'Outros Créditos', false),
    tipoLancamentoFactory(5, 'Outros Débitos', true),
    tipoLancamentoFactory(6, 'Gain day trade', false),
    tipoLancamentoFactory(7, 'Loss day trade', true),
]

const selectCompraOrVenda = (trade) => {
    if(trade.compra){
       return tiposLancamentos()[0] 
    } 
    if(trade.venda){
       return tiposLancamentos()[1] 
    } 
    if(trade.gain){
        return tiposLancamentos()[6] 
    } 
    if(trade.loss){
        return tiposLancamentos()[7] 
    } 
} 

module.exports = {
    tiposLancamentos,
    selectCompraOrVenda
}