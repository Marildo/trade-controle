const { ApolloServer, gql } = require('apollo-server')

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
        carteira:Carteira

        acao:Acao
    }

`

const resolvers = {
    Query: {
        helo() {
            return `Api rodando!  ${new Date}`
        },

        carteira() {
            return {
                id: '12',
                nome: 'Modal'
            }
        },

        acao() {
            return {
                id:10,
                sigla:'LCAM3',
                empresa: 'Locamerica',
                cotacao: '18.90'
            }
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