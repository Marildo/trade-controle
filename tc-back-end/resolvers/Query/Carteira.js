const  carteiraModel  = require('../../model/carteiraModel')

const carteiras = () => {
    return carteiraModel.findAll()
}

const carteira = (parent, args, context) => {
    return carteiraModel.findById(args.id)        
}

module.exports = {
    carteira,
    carteiras
}