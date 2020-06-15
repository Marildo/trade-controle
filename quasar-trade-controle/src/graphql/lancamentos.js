import gql from 'graphql-tag'

const saveTradeAcao = gql`
  mutation(
      $dataCompra: String
      $dataVenda: String
      $quantidade: Int!
      $precoCompra: Float
      $precoVenda: Float
      $corretagem: Float
      $impostos: Float
      $idCarteira:ID!
      $acao:AcaoInput!
  ){ 
    saveTradeAcao(
      dados:{
        dataCompra: $dataCompra
        dataVenda: $dataVenda
        quantidade: $quantidade
        precoCompra: $precoCompra
        precoVenda: $precoVenda
        corretagem: $corretagem
        impostos: $impostos
        idCarteira:$idCarteira
        acao: $acao
      }
    )
    {
      id
      dataMovimentacao
      valor
      descricao
      idCarteira
      tipoLancamento
      {
        key
        descricao
      }
     }
}`

const movimentacoesByIdCarteira = gql`
  query($idCarteira: Int!){
    movimentacoesByIdCarteira(idCarteira: $idCarteira){
      id 
      dataMovimentacao
      valor
      descricao
      idCarteira
      tipoLancamento
      {
        key
        descricao
      }
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
