import gql from 'graphql-tag'

const carteira = gql` query($id: ID!){
  carteira (id: $id) {
    id
    nome
    saldoCaixa
    saldoAcoes
    portifolio {
      quantidade 
      precoMedio 
      totalAtual 
      custoTotal 
      resultado 
      percentual
      idAcao
      codigoAcao
      cotacao
      idSetor
      idSubsetor
      idSegmento
    }
  }
}`

const carteiras = gql` query{
  carteiras {
   id
   nome
   saldoCaixa
   saldoAcoes
  }
}`

export {
  carteira,
  carteiras
}
