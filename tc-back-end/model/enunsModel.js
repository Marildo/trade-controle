function tipoLancamentoFactory(key, descricao, isSaida) {
    return {
        key,
        descricao,
        isSaida
    }
}

const tiposLancamentos = () => [
    tipoLancamentoFactory(0, 'Compra', false),
    tipoLancamentoFactory(1, 'Venda', true),
    tipoLancamentoFactory(2, 'Aporte', false),
    tipoLancamentoFactory(3, 'Retirada', true),
    tipoLancamentoFactory(4, 'Outros Créditos', false),
    tipoLancamentoFactory(5, 'Outros Débitos', true),
]

const selectCompraOrVenda = (isCompra) => tiposLancamentos()[Number(!isCompra)]

module.exports = {
    tiposLancamentos,
    selectCompraOrVenda
}