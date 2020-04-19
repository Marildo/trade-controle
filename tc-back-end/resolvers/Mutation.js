const {acoes, carteiras, nextId} = require('../data/db')

module.exports = {
    newAcao(_,{sigla}){
        const acao = {
            id: nextId,
            sigla,
            empresa: sigla+' ON',
            cotacao: 3.33,
            carteira_id :  Math.floor(Math.random() * (3 - 1) + 1 )            
        }

        acoes.push(acao)
        return acao
    },

    newCarteira(_, {nome}) {
        const carteria = {
            id: nextId,
            nome
        }

        carteiras.push(carteria)
        return carteria
    }
}