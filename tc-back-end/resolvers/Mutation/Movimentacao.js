const {MovimentacaoModel} = require('../../model/')

const model = new MovimentacaoModel

module.exports = {
    saveMovimentacao(_, {tipo,valor,descricao,idCarteira}) {
         const movimentacao = {
             tipo,
             valor,
             descricao,
             carteira_id: idCarteira             
         }
         return model.save(movimentacao)         
    }
} 