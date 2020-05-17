const { TradeAcaoModel, MovimentacaoModel } = require('../../model/')
const { selectCompraOrVenda } = require('../../model/enunsModel')
const {formateReal} = require('../../lib/numberUtils')


// TODO validar se acao e carteiras existem

async function saveTradeAcao(_, { dados }) {
    try {
        let data_trade = dados.dataTrade

        if (data_trade) {
            if (!isNaN(data_trade)) {
                data_trade = new Date(parseInt(data_trade))
            }
            if (!Date.parse(data_trade))
                return new Error("Data inválida")
        }
        

        const tipo = selectCompraOrVenda(dados.compra)
        const descricao = `${tipo.descricao} de ${dados.acao.codigo} (${dados.quantidade} X ${formateReal(dados.valor)})`

        const movimentacao = {
            tipo: tipo.key,
            valor: dados.valor * dados.quantidade,
            carteira_id: dados.idCarteira,
            data_movimentacao: data_trade,
            descricao
        }

        const mov = await new MovimentacaoModel().save(movimentacao)

        console.log(mov)

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

        await new TradeAcaoModel().save(trade)
       .catch( error => new MovimentacaoModel().deleteById(mov.id))

        return mov
    } catch (error) {
        throw new Error(error.sqlMessage)
    }
}

module.exports = {
    saveTradeAcao
}