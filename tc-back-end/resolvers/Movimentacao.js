const { tiposLancamentos } = require('../model/enunsModel')

module.exports = {
    dataMovimentacao(movimentacao) {
        return movimentacao.data_movimentacao
    },

    idCarteira(movimentacao) {
        return movimentacao.carteira_id
    },

    tipoLancamento(movimentacao) {
        const tipo = tiposLancamentos().filter(i => i.key == movimentacao.tipo)
        return tipo[0]
    }
}