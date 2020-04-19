const { acaoModel } = require('../../model/')
const { locateAcao, findCotacao } = require('../../service/Uol')

module.exports = {
    async  newAcao(_, { sigla }) {
        try {
            let find = await acaoModel()
                .where('sigla', sigla.toUpperCase())
                .first()

            if (find) {
                return find
            }

            find = await locateAcao(sigla);
            if (!find) {
                return new Error("Ação não localizada!")
            }

            let price =null;
            const cotacao = await findCotacao(find.idt)
            if(cotacao){
                price = cotacao.price;
            }
            
            const acao = {
                id: find.idt,
                sigla: find.code,
                empresa: find.name,
                cotacao: price,
            }

            const result = await acaoModel()
                .insert(acao)
                .returning('*')

            return result[0]
        } catch (e) {
            console.log(e)
            return new Error(e.sqlMessage)
        }
    },
}