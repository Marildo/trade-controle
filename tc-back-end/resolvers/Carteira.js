const { carteiraModel, summaryAcoesModel } = require('../model')

const makePortifolio = (summary) => {
    const { quantidade, preco_medio, acao_id, codigo, preco,
        setor_id, subsetor_id, segmento_id } = summary

    const totalAtual = (quantidade * preco).toFixed(2)
    const custoTotal = (quantidade * preco_medio).toFixed(2)
    const resultado = (totalAtual - custoTotal).toFixed(2)
    const percentual = ((totalAtual * 100 / custoTotal) - 100).toFixed(2)

    return {
        quantidade,
        precoMedio: preco_medio,
        totalAtual,
        custoTotal,
        resultado,
        percentual,
        idAcao: acao_id,
        codigoAcao: codigo,
        cotacao: preco,
        idSetor: setor_id,
        idSubsetor: subsetor_id,
        idSegmento: segmento_id
    }
}

//TODO tem alguma maneira de ultilizar o resolver acao?
const portifolio = async (carteira) => {
    const summarys = await summaryAcoesModel.findAllByIdCarteira(carteira.id)
    return summarys.map(t => makePortifolio(t))
}

function saldoCaixa(carteira) {
    return carteira.saldo_caixa
}

function saldoAtivos(carteira) {
    return carteira.saldo_ativos
}

function resultadoDiario(carteira) {  
    return carteira.resultado_diario || 0
}

function resultadoSemanal(carteira) {  
    return carteira.resultado_semanal || 0
}

function resultadoMensal(carteira) {  
    return carteira.resultado_mensal || 0
}

function resultadoAnual(carteira) {  
    return carteira.resultado_anual || 0
}

function resultadoTotal(carteira) {  
    return carteira.resultado_total || 0
}

module.exports = {
    portifolio,
    saldoCaixa,
    saldoAtivos,
    resultadoDiario,
    resultadoSemanal,
    resultadoMensal,
    resultadoAnual,
    resultadoTotal
}