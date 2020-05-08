const { TradeAcaoModel, MovimentacaoModel } = require('../../model/')
const { selectCompraOrVenda } = require('../../model/enunsModel')


// TODO validar se acao e carteiras existem

async function saveTradeAcao(_, { dados }) {

    let data_trade = dados.dataTrade

    if (data_trade) {
        if (!isNaN(data_trade)) {
            data_trade = new Date(parseInt(data_trade))
        }
        if (!Date.parse(data_trade))
            return new Error("Data inválida")
    }

    const tipo = selectCompraOrVenda(dados.compra)
    const descricao = `${tipo.descricao} de ${dados.acao.codigo}`

    const movimentacao = {
        tipo: tipo.key,
        valor: dados.valor,
        carteira_id: dados.idCarteira,
        data_movimentacao: data_trade,
        descricao
    }

    const mov = await new MovimentacaoModel().save(movimentacao)

    const trade = {
        ...dados,
        data_trade,
        acao_id: dados.acao.id,
        carteira_id: dados.idCarteira,
        movimentacao_id: mov.id
    }

    delete trade.dataTrade
    delete trade.acao
    delete trade.idCarteira

    return new TradeAcaoModel().save(trade)
}

module.exports = {
    saveTradeAcao
}