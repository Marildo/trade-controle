const carteiras = [
    {
        id: 1,
        nome: 'Modal'
    },
    {
        id: 2,
        nome: 'Pioneiros'
    },
    {
        id: 3,
        nome: 'Buy Holder'
    }
]

const acoes = [
    {
        id: 10,
        sigla: 'LCAM3',
        empresa: 'Locamerica',
        cotacao: '18.90',
        carteira_id: 1
    },
    {
        id: 01,
        sigla: 'IRBR3',
        empresa: 'IRBBRASIL',
        cotacao: '11,20',
        carteira_id: 2
    },
    {
        id: 05,
        sigla: 'VVAR3',
        empresa: 'VIAVAREJO ',
        cotacao: '7,25',
        carteira_id: 3
    },
    {
        id: 04,
        sigla: 'CIEL3',
        empresa: 'Cielo ',
        cotacao: '7,25',
        carteira_id: 2
    }
]

module.exports = {
    carteiras,
    acoes
}