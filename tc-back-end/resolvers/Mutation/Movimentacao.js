const { MovimentacaoModel,TradeAcaoModel, SummaryAcoesModel } = require('../../model/')

const model = new MovimentacaoModel

// TODO padronizar retorno de erros pelos codigos
// TODO realizar validacoes

const deleteMovimentacao = async (_, {id}) => {
    const tradeModel = new TradeAcaoModel
    const trade =  await tradeModel.findByMovimentacaoId(id)
    if(trade != undefined){
        trade.deleting = true
        new SummaryAcoesModel().updateSummary(trade)
    }
    return model.deleteById(id)
}

const saveMovimentacao = (_, { dados }) => {
    try {
        let data_movimentacao = dados.dataMovimentacao
        if (dados.dataMovimentacao) {
            if (!isNaN(dados.dataMovimentacao)) {
                data_movimentacao = new Date(parseInt(data_movimentacao))
            }
            if (!Date.parse(data_movimentacao))
                return new Error("Data inválida")
        }

        const movimentacao = {
            ...dados,
            carteira_id: dados.idCarteira,
            data_movimentacao
        }

        delete movimentacao.idCarteira
        delete movimentacao.dataMovimentacao

        return model.save(movimentacao)
    } catch (error) {
        console.log(error)
        return new Error("Error: " + error.code)
    }
}

module.exports = {
    saveMovimentacao,
    deleteMovimentacao
} 