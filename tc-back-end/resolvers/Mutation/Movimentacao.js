const { MovimentacaoModel } = require('../../model/')

const model = new MovimentacaoModel

// TODO padronizar retorno de erros pelos codigos
module.exports = {
    async saveMovimentacao(_, { dados }) {
        try {
            let data_movimentacao =  dados.dataMovimentacao 
            if (dados.dataMovimentacao) {
                if (!isNaN(dados.dataMovimentacao)) {
                    dados.dataMovimentacao = new Date(parseInt(dados.dataMovimentacao))
                } 
            }

            if(! Date.parse(data_movimentacao))
                return new Error("Data inválida")
                              

            const movimentacao = {
                ...dados,
                carteira_id: dados.idCarteira,
                data_movimentacao
            }

            delete movimentacao.idCarteira
            delete movimentacao.dataMovimentacao

            return await model.save(movimentacao)
        } catch (error) {
            console.log(error)
            return new Error("Error: " + error.code)
        }
    }
} 