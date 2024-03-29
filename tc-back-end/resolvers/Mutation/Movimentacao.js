const {
  movimentacaoModel,
  tradeAcaoModel,
  summaryAcoesModel,
  carteiraModel,
} = require('../../model/')

// TODO padronizar retorno de erros pelos codigos
// TODO realizar validacoes

const deleteMovimentacao = async (_, { id }) => {
  try {
    const mov = await movimentacaoModel.findById(id)

    if (mov) {
      const trade = await tradeAcaoModel.findByMovimentacaoId(id)
      const deleted = await movimentacaoModel.deleteById(id)
     
      if (trade != undefined) {
        await summaryAcoesModel.updateSummary(trade)
      }

      carteiraModel.updateCarteira(mov.carteira_id)

      return deleted
    }
  } catch (error) {
    console.log(error)
    return new Error('Error: ' + error.code)
  }
}

const saveMovimentacao = (_, { dados }) => {
  try {
    let data_movimentacao = dados.dataMovimentacao
    if (dados.dataMovimentacao) {
      if (!isNaN(dados.dataMovimentacao)) {
        data_movimentacao = new Date(parseInt(data_movimentacao))
      }
      if (!Date.parse(data_movimentacao)) return new Error('Data inválida')
    }

    const movimentacao = {
      ...dados,
      carteira_id: dados.idCarteira,
      data_movimentacao,
    }

    carteiraModel.updateCarteira(dados.idCarteira)

    delete movimentacao.idCarteira
    delete movimentacao.dataMovimentacao

    return movimentacaoModel.save(movimentacao)
  } catch (error) {
    console.log(error)
    return new Error('Error: ' + error.code)
  }
}

module.exports = {
  saveMovimentacao,
  deleteMovimentacao,
}
