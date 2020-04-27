const { CarteiraModel } = require('../../model')

const saveCarteira = (_, { nome }) =>{
        const carteira = {
            nome
        }
        const model = new CarteiraModel
        return model.save(carteira)
}

module.exports = {
    saveCarteira
}