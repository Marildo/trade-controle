import gql from 'graphql-tag'
import vue from 'vue'

import store from '@/store';
import { loadCarteira } from './carteiraController'
import { showToastSuccess, catchError } from '@/lib/messages'


function saveTrade(dadosForm) {
    return new Promise((resolve) => {
        const trade = {
            ...dadosForm,
            dataTrade:
                "" +
                new Date(
                    dadosForm.data + " " + dadosForm.hora
                ).getTime()
        }

        return vue.prototype.$api.mutate({
            mutation: gql`
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
            }`,
            variables: {
                ...trade
            }
        })
            .then(resp => resp.data.saveTradeAcao)
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


export {
    saveTrade
}
