import gql from 'graphql-tag'

const carteira = gql`
  query($id: ID!) {
    carteira(id: $id) {
      id
      nome
      saldoCaixa
      saldoAtivos
      resultadoTotal
      resultadoAnual
      resultadoMensal
      resultadoSemanal
      resultadoDiario
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
  }
`

const carteiras = gql`
  query {
    carteiras {
      id
      nome
      saldoCaixa
      saldoAtivos
      resultadoTotal
      resultadoAnual
      resultadoMensal
      resultadoSemanal
      resultadoDiario
    }
  }
`

const saveCarteira = gql`
  mutation ($nome: String!) {
    saveCarteira(nome: $nome){
      id
      nome
    }
  }
`

export { carteira, carteiras, saveCarteira }
