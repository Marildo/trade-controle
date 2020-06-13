import gql from 'graphql-tag'

const acoes = gql` query{
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
}`

export {
  acoes
}
