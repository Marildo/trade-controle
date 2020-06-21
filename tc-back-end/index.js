const dotenv = require('dotenv')
dotenv.config()

// TODO Usar classes e typescript
// TODO - Refatorar sumary de acoes, não esta calculando tudo corretamente

const { ApolloServer } = require('apollo-server')
const { importSchema} = require('graphql-import')

const typeDefs = importSchema('./schema/index.graphql')
const resolvers = require('./resolvers/index')

const server = new ApolloServer({
    typeDefs,
    resolvers
})

server.listen().then(({ url }) => {
    console.log(`Executando em ${url}`)
})

const {updatePrices} = require('./service/acao/updatePrices')
updatePrices()
