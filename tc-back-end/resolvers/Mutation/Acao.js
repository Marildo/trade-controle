const { SetorModel, SubsetorModel, SegmentoModel, AcaoModel } = require('../../model/')
const { findAcao } = require('../../service/acao/Statusinvest')

module.exports = {
    async newAcao(_, { codigo }) {
        try {
            codigo = codigo.toUpperCase()

            let model = new AcaoModel
            const find = await model.findByCodigo(codigo)

            if (find)
                return find

            const papel = await findAcao(codigo);
            if (!papel) {
                return new Error("Ação não localizada!")
            }

            model = new SetorModel
            const setor = await model.save(papel.setor)

            model= new SubsetorModel
            const subsetor = await model.save(papel.subsetor)

            model = new SegmentoModel
            const segmento = await model.save(papel.segmento)
            
            const acao = {
                codigo,
                id: papel.id,
                empresa: papel.empresa,
                preco: papel.preco,
                setor_id: papel.setor.id,
                subsetor_id: papel.subsetor.id,
                segmento_id: papel.segmento.id
            }
      
            model = new AcaoModel
            const result = await model.save(acao)

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