import gql from 'graphql-tag'
import vue from 'vue'

function AcController() {
    this.teste = () => {
        console.log('testanto....')
    }

    this.excluirUsuario = (id) => {
        console.log('delete....')
         vue.prototype.$api.mutate({
            mutation: gql`mutation (
                $id: Int
                $email: String
            ) {
                excluirUsuario (
                    filtro: {
                        id: $id
                        email: $email
                    }
                ) { 
                    id nome email
                }
            }`,
            variables: {
                id
            },
        })
    }
}

module.exports = AcController