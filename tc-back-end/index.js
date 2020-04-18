const { ApolloServer, gql } = require('apollo-server')

const carteiras = [
    {
        id: '12',
        nome: 'Modal'
    },
    {
        id: 10,
        nome: 'Pioneiros'
    },
    {
        id :1,
        nome: 'Buy Holder'
    }
]

const acoes = [
    {
        id: 10,
        sigla: 'LCAM3',
        empresa: 'Locamerica',
        cotacao: '18.90'
    },
    {
        id: 01,
        sigla: 'IRBR3',
        empresa: 'IRBBRASIL',
        cotacao: '11,20'
    },
    {
        id: 05,
        sigla: 'VVAR3',
        empresa: 'VIAVAREJO ',
        cotacao: '7,25'
    }

]

const typeDefs = gql`

    type Carteira{
        id: ID!
        nome: String!
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
    }
}

const server = new ApolloServer({
    typeDefs,
    resolvers
})

server.listen().then(({ url }) => {
    console.log(`Executando em ${url}`)
})