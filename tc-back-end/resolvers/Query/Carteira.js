const {carteiraModel} = require('../../config/model')

// TODO Alterar para async/await ?
module.exports = {
    carteira(_, args) {
        return carteiraModel()
            .where('id', args.id)
            .first()
            .catch((e) => console.log(e))
    },
    carteiras() {      
        return carteiraModel()
            .catch((e) => console.log(e))
    },
}