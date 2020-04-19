const {carteiraModel} = require('../../config/model')

module.exports = {
    async newCarteira(_, { nome }) {
        try {
            const carteira = {
                nome
            }

            const [id] = await carteiraModel()
                .insert(carteira)
                .returning('id')

            return result = {
                ...carteira,
                id
            }
        } catch (e) {
            console.log(e)
            throw new Error(e.detail)
        }
    }
}