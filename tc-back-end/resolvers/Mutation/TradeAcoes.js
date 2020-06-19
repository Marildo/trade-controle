const { TradeAcaoModel, MovimentacaoModel, SummaryAcoesModel } = require('../../model/')
const { selectCompraOrVenda } = require('../../model/enunsModel')
const { formateReal } = require('../../lib/numberUtils')

// TODO validar se acao e carteiras existem

async function saveTradeAcao(_, { dados }) {
    try {
        const compra = dados.precoCompra > 0  && (isNaN(dados.precoVenda) || dados.precoVenda == 0)
        const venda = dados.precoVenda > 0  && (isNaN(dados.precoCompra) || dados.precoCompra == 0)
        const gain = !compra && !venda && dados.precoVenda > dados.precoCompra
        const loss = !compra && !venda && dados.precoVenda <= dados.precoCompra

        let data_compra = dados.dataCompra
        if (compra || gain || loss) {
            if (!isNaN(data_compra)) {
                data_compra = new Date(parseInt(data_compra))
            }
            if (!Date.parse(data_compra))
                return new Error("Data inválida")
        }

        let data_venda = dados.dataVenda
        if (venda || gain || loss) {
            if (!isNaN(data_venda)) {
                data_venda = new Date(parseInt(data_venda))
            }
            if (!Date.parse(data_venda))
                return new Error("Data inválida")
        }

        let valorUnitario = 0
        let valor = 0
        if (compra) {
            valor = dados.quantidade * dados.precoCompra
            valorUnitario = dados.precoCompra
        } else if (venda) {
            valor = dados.quantidade * dados.precoVenda
            valorUnitario = dados.precoVenda
        } else {
            valor = (dados.quantidade * dados.precoCompra) - (dados.quantidade * dados.precoVenda)
        }

        const tipo = selectCompraOrVenda({compra, venda, gain, loss})
        const descricao = `${tipo.descricao} de ${dados.acao.codigo} (${dados.quantidade} X ${formateReal(valorUnitario)})`

        const movimentacao = {
            tipo: tipo.key,
            valor,
            carteira_id: dados.idCarteira,
            data_movimentacao: data_compra || data_venda,
            descricao
        }

        const mov = await new MovimentacaoModel().save(movimentacao)

        const trade = {
            compra,
            venda,
            preco_venda: dados.precoVenda,
            preco_compra: dados.precoCompra,
            quantidade: dados.quantidade,
            data_compra,
            data_venda,
            finalizada: gain || loss,
            acao_id: dados.acao.id,
            carteira_id: dados.idCarteira,
            movimentacao_id: mov.id
        }

        await new TradeAcaoModel().save(trade)
        await new SummaryAcoesModel().updateSummary(dados)

        return mov
    } catch (error) {
        
        console.log(error)
        throw new Error(error)
    }
}

module.exports = {
    saveTradeAcao
}