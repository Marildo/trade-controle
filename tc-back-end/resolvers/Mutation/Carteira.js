const { carteiraModel } = require('../../model')

const saveCarteira = (_, { nome }) =>{
    return carteiraModel.save({nome})
}

module.exports = {
    saveCarteira
}