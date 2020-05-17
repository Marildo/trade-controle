import gql from 'graphql-tag'
import vue from 'vue'
import store from './../store/'
import { showToastSuccess, catchError } from '@/lib/messages'
import { loadCarteira } from './carteiraController'


const loadLancamentos = (idCarteira) => {
    vue.prototype.$api.query({
        query: gql` query($idCarteira: Int!){
                    movimentacoesByIdCarteira(idCarteira: $idCarteira){
                        id dataMovimentacao valor descricao idCarteira
                        tipoLancamento {key descricao}
                    }
                }`,
        variables: {
            idCarteira: parseInt(idCarteira)
        }
    })
        .then(resp => resp.data.movimentacoesByIdCarteira)
        .then(lancamentos => store.commit('lancamentos', lancamentos))
        .catch(error => catchError(error))
}

const saveLancamento = (lancamento) => {
    return new Promise((resolve) => {
        vue.prototype.$api.mutate({
            mutation: gql` mutation(
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
                        id dataMovimentacao valor descricao idCarteira
                        tipoLancamento {key descricao}
                    }      
            }`,
            variables: {
                ...lancamento
            }
        })
            .then(resp => resp.data.saveMovimentacao)
            .then(lancamento => {
                store.dispatch('addLancamento', lancamento)
                showToastSuccess()
                resolve(lancamento)
                return lancamento.idCarteira
            })
            .then(id => loadCarteira(id))
            .catch(error => catchError(error))
    })
}

const deleteLancamento = (lancamento) => {
    vue.prototype.$api.mutate({
        mutation: gql` mutation($id: ID!){
            deleteMovimentacao(id :$id)
        }`,
        variables: {
            id: lancamento.id
        }
    })       
        .then(() => showToastSuccess())
        .then(() => store.dispatch('deleteLancamento', lancamento))    
        .then(() => loadCarteira(lancamento.idCarteira))
        .catch(error => catchError(error))
}


export {
    loadLancamentos,
    saveLancamento,
    deleteLancamento
}

