const {  acaoModel, setorModel } = require('../../model/')
const { findAcao } = require('../../service/acao/Statusinvest')

module.exports = {
    async newAcao(_, { codigo }) {
        try {
            codigo = codigo.toUpperCase()

            const find = await acaoModel.findByCodigo(codigo)

            if (find)
                return find

            const papel = await findAcao(codigo);
            if (!papel) {
                return new Error("Ação não localizada!")
            }
            
            const setor = await setorModel.saveSetor(papel.setor)
            const subsetor = await setorModel.saveSubSetor(papel.subsetor)
            const segmento = await setorModel.saveSegmento(papel.segmento)
            
            const acao = {
                codigo,
                id: papel.id,
                empresa: papel.empresa,
                preco: papel.preco,
                setor_id: papel.setor.id,
                subsetor_id: papel.subsetor.id,
                segmento_id: papel.segmento.id
            }
      
            const result = await acaoModel.save(acao)
            const newAcao = {
                setor: papel.setor.nome,
                subsetor: papel.subsetor.nome,
                segmento: papel.segmento.nome,
                ...result
            }

            return newAcao
        } catch (e) {
            console.log(e)
            return new Error(e)
        }
    },
}