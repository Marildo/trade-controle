const { acaoModel } = require('../../config/model')

module.exports = {
    async  newAcao(_, { sigla }) {
        try {
            const acao = {
                sigla,
                empresa: sigla + ' ON',
                cotacao: 3.33,
            }

            const result = await acaoModel()
                .insert(acao)
                .returning('*')

            return result[0]
        } catch (e) {
            console.log(e)
        }
    },
}