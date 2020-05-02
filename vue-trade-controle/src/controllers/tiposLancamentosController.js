import gql from 'graphql-tag'
import vue from 'vue'

const findAllTipos = () => {
    return vue.prototype.$api.query({
        query: gql `
        query{
            tiposLancamentos{ key descricao isSaida}
        }`
    })
}

export { findAllTipos }