const { tiposLancamentos } = require('../model/enunsModel')

module.exports = {
    dataMovimentacao(movimentacao) {
        return movimentacao.data_movimentacao
    },

    tipoLancamento(movimentacao) {
        const tipo = tiposLancamentos().filter(i => i.key == movimentacao.tipo)
        return tipo[0]
    }
}