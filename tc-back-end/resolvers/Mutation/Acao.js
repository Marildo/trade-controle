const { acaoModel } = require('../../model/')
const {findAcao} = require('../../service/acao/Statusinvest')

module.exports = {
    async  newAcao(_, { codigo }) {
        try {
            codigo = codigo.toUpperCase()

            let find = await acaoModel()
                .where('codigo', codigo)
                .first()

            if (find) {
                return find
            }

             const papel = await findAcao(codigo);
            console.log(papel)
            if (!papel) {
                return new Error("Ação não localizada!")
            }
            
            const acao = {
                codigo,
                id: papel.id,              
                empresa: papel.empresa,
                preco: papel.preco,
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