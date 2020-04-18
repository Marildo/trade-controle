const { ApolloServer, gql } = require('apollo-server')

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
        id :3,
        nome: 'Buy Holder'
    }
]

const acoes = [
    {
        id: 10,
        sigla: 'LCAM3',
        empresa: 'Locamerica',
        cotacao: '18.90',
        carteira_id:1
    },
    {
        id: 01,
        sigla: 'IRBR3',
        empresa: 'IRBBRASIL',
        cotacao: '11,20',
        carteira_id:2
    },
    {
        id: 05,
        sigla: 'VVAR3',
        empresa: 'VIAVAREJO ',
        cotacao: '7,25',
        carteira_id:3
    },
    {
        id: 04,
        sigla: 'CIEL3',
        empresa: 'Cielo ',
        cotacao: '7,25',
        carteira_id:2
    }
]

const typeDefs = gql`

    type Carteira{
        id: ID!
        nome: String!
        acoes:[Acao]
    }

    type Acao {
        id:ID!
        sigla:String!
        empresa:String!
        cotacao:Float
    }

    type Query{
        helo:String

        carteira(id:ID):Carteira
        carteiras:[Carteira]!

        acao(id:ID):Acao
        acoes:[Acao]!
    }

`

const resolvers = {
    Query: {
        helo() {
            return `Api rodando!  ${new Date}`
        },

        carteira(_, args) {
            const selected = carteiras.filter(a => a.id == args.id)
            return  selected ? selected[0]: null
        },

        carteiras(){
            return carteiras
        },

        acao(_,args) {
            const selected = acoes.filter(a => a.id == args.id)
            return  selected ? selected[0]: null
        },

        acoes() {
            return acoes
        }
    },

    Carteira:{
        acoes(carteira){
            const selected = acoes.filter(a => a.carteira_id == carteira.id )
            return selected ? selected: null
        }
    }
}

const server = new ApolloServer({
    typeDefs,
    resolvers
})

server.listen().then(({ url }) => {
    console.log(`Executando em ${url}`)
})