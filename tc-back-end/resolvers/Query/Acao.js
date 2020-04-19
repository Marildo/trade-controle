const acoes = []

module.exports = {
    acao(_, args) {
        const selected = acoes.filter(a => a.id == args.id)
        return selected ? selected[0] : null
    },
    acoes() {
        return acoes
    }
}