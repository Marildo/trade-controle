const { acaoModel } = require('../../model')

module.exports = {
    acao(_, args) {
        return acaoModel()
            .where('id', args.id)
            .first()
            .catch((e) => console.log(e))
    },
    acoes() {
        return acaoModel()
            .catch((e) => console.log(e))
    }
}