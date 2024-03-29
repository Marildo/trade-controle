import Vue from 'vue'
import { ApolloClient } from 'apollo-client'
import { createHttpLink } from 'apollo-link-http'
import { setContext } from 'apollo-link-context'
import { InMemoryCache } from 'apollo-cache-inmemory'

Vue.use({
  install (Vue) {
    const httpLink = createHttpLink({
      uri: 'http://localhost:4000/'
    })

    const authLink = setContext((_, { headers }) => {
      const token = localStorage.getItem('token')
      return {
        headers: {
          ...headers,
          authorization: token ? `Bearer ${token}` : ''
        }
      }
    })

    Vue.prototype.$apollo = new ApolloClient({
      link: authLink.concat(httpLink),
      cache: new InMemoryCache(),
      onError: ({ graphQLErrors, networkError }) => {
        if (graphQLErrors) {
          graphQLErrors.map(({ message, locations, path }) =>
            console.log(
              `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`
            )
          )
        }
        if (networkError) {
          if (networkError.statusCode === 401) {
            window.location.href = '/api/security/logout'
          }
          console.log(`[Network error]: ${networkError}`)
        }
      }
    })
  }
})
