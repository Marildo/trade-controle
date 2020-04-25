const { acaoModel } = require('../../model/')
const { saveSetor, saveSubsetor, saveSegmento } = require('../../model/simpleModel')
const { findAcao } = require('../../service/acao/Statusinvest')

module.exports = {
    async newAcao(_, { codigo }) {
        try {
            codigo = codigo.toUpperCase()


            let find = await acaoModel()
                .where('codigo', codigo)
                .first()

            if (find) {
                return find
            }

            const papel = await findAcao(codigo);
            if (!papel) {
                return new Error("Ação não localizada!")
            }

            const acao = {
                codigo,
                id: papel.id,
                empresa: papel.empresa,
                preco: papel.preco,
                setor_id: papel.setor.id,
                subsetor_id: papel.subsetor.id,
                segmento_id: papel.segmento.id
            }

            await saveSegmento(papel.segmento)
            await saveSubsetor(papel.subsetor)
            await saveSetor(papel.setor)

            //TODO alterar retorno para trazer consulta completa com nomes de setores
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