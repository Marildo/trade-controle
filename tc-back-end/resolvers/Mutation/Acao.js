const { acaoModel } = require('../../model/')
const {findAcao} = require('../../service/acao/Statusinvest')

module.exports = {
    async  newAcao(_, { sigla }) {
        try {
            sigla = sigla.toUpperCase()

            let find = await acaoModel()
                .where('sigla', sigla)
                .first()

            if (find) {
                return find
            }

             const papel = await findAcao(sigla);
            console.log(papel)
            if (!papel) {
                return new Error("Ação não localizada!")
            }
            
            const acao = {
                sigla: sigla.toUpperCase(),
                id: papel.id,              
                empresa: papel.empresa,
                cotacao: papel.preco,
            }

           const result = await acaoModel()
                .insert(acao)
                .returning('*')
                   return result[0]         
        } catch (e) {
            console.log(e)
            return new Error(e)
        }
    },
}