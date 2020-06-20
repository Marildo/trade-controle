import gql from 'graphql-tag'

const acoes = gql`
  query {
    acoes {
      id
      codigo
      empresa
      preco
      setor {
        id
        nome
      }
      subsetor {
        id
        nome
      }
      segmento {
        id
        nome
      }
    }
  }
`
const newAcao = gql`
  mutation ($codigo: String!) {
    newAcao(codigo: $codigo){
      codigo
    }
  }
`

export { acoes, newAcao }
