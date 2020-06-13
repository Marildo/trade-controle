import gql from 'graphql-tag'

const saveTradeAcao = gql`
  mutation(
      $dataTrade: String!
      $compra: Boolean!
      $quantidade: Int!
      $valor: Float!
      $corretagem: Float
      $impostos: Float
      $idCarteira:ID!
      $acao:AcaoInput!
  ){ 
    saveTradeAcao(
        dados:{
            dataTrade: $dataTrade
            compra: $compra
            quantidade: $quantidade
            valor: $valor
            corretagem: $corretagem
            impostos: $impostos
            idCarteira:$idCarteira
            acao: $acao
        }
    ){
        id dataMovimentacao valor descricao idCarteira
        tipoLancamento {key descricao}
     }
}`

const movimentacoesByIdCarteira = gql`
  query($idCarteira: Int!){
    movimentacoesByIdCarteira(idCarteira: $idCarteira){
      id dataMovimentacao valor descricao idCarteira
      tipoLancamento {key descricao}
  }
}`

const deleteMovimentacao = gql` 
  mutation($id: ID!){
    deleteMovimentacao(id :$id)
}`

export {
  saveTradeAcao,
  movimentacoesByIdCarteira,
  deleteMovimentacao
}
