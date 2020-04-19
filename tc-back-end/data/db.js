let id = 1;

function nextId(){
    return id++
}

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
        id: nextId(),
        sigla: 'LCAM3',
        empresa: 'Locamerica',
        cotacao: '18.90',
        carteira_id: 1
    },
    {
        id: nextId(),
        sigla: 'IRBR3',
        empresa: 'IRBBRASIL',
        cotacao: '11,20',
        carteira_id: 2
    },
    {
        id: nextId(),
        sigla: 'VVAR3',
        empresa: 'VIAVAREJO ',
        cotacao: '7,25',
        carteira_id: 3
    },
    {
        id: nextId(),
        sigla: 'CIEL3',
        empresa: 'Cielo ',
        cotacao: '7,25',
        carteira_id: 2
    }
]

module.exports = {
    carteiras,
    acoes,
    nextId
}