const {carteiraModel} = require('../../config/model')

module.exports = {
    async newCarteira(_, { nome }) {
        try {
            const carteira = {
                nome
            }

            const result = await carteiraModel()
                .insert(carteira)
                .returning('*')

            return result[0]
        } catch (e) {
            console.log(e)
            throw new Error(e.detail)
        }
    }
}