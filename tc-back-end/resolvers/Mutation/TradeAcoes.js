const { TradeAcaoModel, MovimentacaoModel, SummaryAcoesModel } = require('../../model/')
const { selectCompraOrVenda } = require('../../model/enunsModel')
const { formateReal } = require('../../lib/numberUtils')

// TODO validar se acao e carteiras existem



async function saveTradeAcao(_, { dados }) {
    try {
        dados.compra = dados.precoCompra > 0  && (isNaN(dados.precoVenda) || dados.precoVenda == 0)
        dados.venda = dados.precoVenda > 0  && (isNaN(dados.precoCompra) || dados.precoCompra == 0)
        dados.gain = !dados.compra && !dados.venda && dados.precoVenda > dados.precoCompra
        dados.loss = !dados.compra && !dados.venda && dados.precoVenda <= dados.precoCompra

        let data_compra = dados.dataCompra
        if (dados.compra || dados.gain || dados.loss) {
            if (!isNaN(data_compra)) {
                data_compra = new Date(parseInt(data_compra))
            }
            if (!Date.parse(data_compra))
                return new Error("Data inválida")
        }

        let data_venda = dados.dataVenda
        if (dados.venda || dados.gain || dados.loss) {
            if (!isNaN(data_venda)) {
                data_venda = new Date(parseInt(data_venda))
            }
            if (!Date.parse(data_venda))
                return new Error("Data inválida")
        }

        let valor = 0
        if (dados.compra) {
            valor = dados.quantidade * dados.precoCompra
        } else if (dados.venda) {
            valor = dados.quantidade * dados.precoVenda
        } else {
            valor = (dados.quantidade * dados.precoCompra) - (dados.quantidade * dados.precoVenda)
        }

        const tipo = selectCompraOrVenda(dados)
        const descricao = `${tipo.descricao} de ${dados.acao.codigo} (${dados.quantidade} X ${formateReal(valor)})`

        const movimentacao = {
            tipo: tipo.key,
            valor,
            carteira_id: dados.idCarteira,
            data_movimentacao: data_compra || data_venda,
            descricao
        }

        const mov = await new MovimentacaoModel().save(movimentacao)

        const trade = {
            preco_venda: dados.precoVenda,
            preco_compra: dados.precoCompra,
            quantidade: dados.quantidade,
            data_compra,
            data_venda,
            finalizada: dados.gain || dados.loss,
            acao_id: dados.acao.id,
            carteira_id: dados.idCarteira,
            movimentacao_id: mov.id
        }

        const tradeModel = new TradeAcaoModel()
        await tradeModel
            .save(trade)
            .catch(() => new MovimentacaoModel().deleteById(mov.id))

        new SummaryAcoesModel().updateSummary(dados)

        return mov
    } catch (error) {
        console.log(error)
        throw new Error(error)
    }
}

module.exports = {
    saveTradeAcao
}