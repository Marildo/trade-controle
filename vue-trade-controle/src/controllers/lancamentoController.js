import gql from 'graphql-tag'
import vue from 'vue'

function LancamentoController() {
    this.findByCarteiraId = (idCarteira) => {
        return new Promise((resolve, reject) => {
            vue.prototype.$api.query({
                query: gql`
                query($idCarteira: Int!){
                    movimentacoesByIdCarteira(idCarteira: $idCarteira){
                        id dataMovimentacao valor descricao 
                        tipoLancamento {key descricao}
                    }
                }`,
                variables:{
                    idCarteira:  parseInt(idCarteira)
                }
            })
                .catch(error =>{
                    console.log(error.networkError.result.errors)
                    reject(error)
                })
                .then(resp =>{
                    resolve(resp.data.movimentacoesByIdCarteira)
                    vue.prototype.$api.resetStore()
                })
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
                        id dataMovimentacao valor descricao
                        tipoLancamento {key descricao}
                    }      
            }`,
                    variables: {
                        ...lancamento
                    }
                })
                    .catch(error => reject(error))
                    .then(resp => {
                        resolve(resp)
                       // vue.prototype.$api.resetStore()
                    })

            })
        }
}

export default LancamentoController