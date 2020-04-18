const { ApolloServer, gql } = require('apollo-server')

const typeDefs = gql`
    type Query{
        helo:String
    }
`

const resolvers = {
    Query:{
        helo(){
            return `Api rodando!  ${new Date}`
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