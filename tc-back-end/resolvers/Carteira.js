const acoes = [];

module.exports = {
    acoes(carteira) {
        const selected = acoes.filter(a => a.carteira_id == carteira.id)
        return selected ? selected : null
    },
}