import gql from 'graphql-tag'
import vue from 'vue'
import store from './../store/'

import { catchError } from '@/lib/messages'

const loadTipoLancamentos = () => {
    return vue.prototype.$api.query({
        query: gql`
        query{
            tiposLancamentos{ key descricao isSaida}
        }`
    })
        .then(resp => resp.data.tiposLancamentos)
        .then(tipos => store.commit("tiposLancamentos", tipos.filter(t => parseInt(t.key) >= 2)))
        .catch(error => catchError(error));
}

export { loadTipoLancamentos }