import gql from 'graphql-tag'
import vue from 'vue'

function LancamentoController() {
    this.findByCarteiraId = () => {
        return vue.prototype.$api.query({
            query: gql`{
                movimentacoes{
                    id dataMovimentacao valor descricao tipo
                }
            }`
        })
    },

    this.save = (lancamento) => {
        return vue.prototype.$api.mutate({
            mutation: gql`
            mutation(
                $tipo: Int!
                $valor: Float!
                $idCarteira: Int!
                $descricao: String
                $dataMovimentacao: String                    
                 ){
                    saveMovimentacao(
                        dados:{
                            tipo: $tipo
                            valor: $valor
                            idCarteira: $idCarteira
                            descricao: $descricao
                            dataMovimentacao: $dataMovimentacao 
                        }
                    ) {
                        id dataMovimentacao valor descricao tipo
                    }      
            }`,
            variables: {
              ...lancamento
            }
        })
    }
}

export default LancamentoController