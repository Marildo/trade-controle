const { ApolloServer, gql } = require('apollo-server')

const typeDefs = gql`

    type Carteira{
        id: ID
        nome: String
    }

    type Query{
        helo:String
        carteira:Carteira
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