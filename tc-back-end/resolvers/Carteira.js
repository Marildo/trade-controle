const { CarteiraModel, SummaryAcoesModel } = require('../model')

const makePortifolio = (summary) => {
    const { quantidade, preco_medio,preco_atual, resultado, percentual,
        acao_id, codigo, preco, setor_id, subsetor_id, segmento_id } = summary
    return {
        quantidade,
        resultado,
        percentual,
        precoAtual: preco_atual,
        precoMedio: preco_medio,
        idAcao: acao_id,
        codigoAcao: codigo,
        currentPrice: preco,
        idSetor: setor_id,
        idSubsetor: subsetor_id,
        idSegmento: segmento_id
    }
}

//TODO tem alguma maneira de ultilizar o resolver acao?
const portifolio = async (carteira) => {
    const trades = await new SummaryAcoesModel().findAllByIdCarteira(carteira.id)
    return trades.map(t => makePortifolio(t))
}

function saldoCaixa(carteira) {
    const carteiraModel = new CarteiraModel
    return carteiraModel.calculateSaldoCaixa(carteira.id)
}

function saldoAcoes(carteira) {
    const carteiraModel = new CarteiraModel
    return carteiraModel.calculateSaldoAcoes(carteira.id)
}

module.exports = {
    portifolio,
    saldoCaixa,
    saldoAcoes
}