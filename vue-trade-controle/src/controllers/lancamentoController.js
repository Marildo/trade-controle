import gql from 'graphql-tag'
import vue from 'vue'

// TODO passar paramentro
function LancamentoController() {

    this.findByCarteiraId = () => {
        return new Promise((resolve, reject) => {
            vue.prototype.$api.query({
                query: gql`
                query{
                    movimentacoes{
                        id dataMovimentacao valor descricao tipo
                    }
                }`
            })
                .catch(error => reject(error))
                .then(resp => resolve(resp.data.movimentacoes))

        })
    },

        this.save = (lancamento) => {
            return new Promise((resolve, reject) => {
                vue.prototype.$api.mutate({
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
                    .catch(error => reject(error))
                    .then(resp => {
                        resolve(resp)
                        vue.prototype.$api.resetStore()
                    })

            })
        }
}

export default LancamentoController