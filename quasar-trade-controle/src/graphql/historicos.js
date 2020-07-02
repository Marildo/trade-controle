import gql from 'graphql-tag'

const historicoLastMonthGroupByData = gql`
  query {
    historicoLastMonthGroupByData {
      title
      dataHistorico
      saldoAtivos
      saldoCaixa
    }
  }
`

export { historicoLastMonthGroupByData }
