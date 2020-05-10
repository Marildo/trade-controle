import gql from 'graphql-tag'
import vue from 'vue'
import store from './../store/';

// TODO deixar gql em arquivos separados
// TODO usar fragmentos
function AcaoController() {

  this.loadAcoes =  () => {
    vue.prototype.$api.query({
      query: gql`
           query{
              acoes {
                id
                codigo
                empresa
                preco
                setor {
                  id
                  nome
                }
                subsetor {
                  id
                  nome
                }
              }
            }
          `
    })
    .then(resp => store.commit('setAcoes', resp.data.acoes))
      .catch(error => {
        console.log(error)
        console.log(error.networkError.result.errors)
      })
  },

    this.save = function (_codigo) {
      return vue.prototype.$api.mutate({
        mutation: gql`
          mutation($codigo: String!) {
            newAcao(codigo: $codigo) {
              id
              codigo
            }
          }
        `,
        variables: {
          codigo: _codigo
        }
      });
    },

    this.findByCodigo = function (codigo) {
      return vue.prototype.$api.query({
        query: gql`
          query($codigo: String!) {
            acao(codigo: $codigo) {
              codigo
              empresa
              preco
              setor {
                id
                nome
              }
              subsetor {
                id
                nome
              }
            }
          }
        `,
        variables: {
          codigo
        }
      });
    },

    this.fields = () => {
      return [
        {
          text: "Código",
          align: "start",
          sortable: true,
          value: "codigo"
        },
        {
          text: "Empresa",
          align: "start",
          sortable: false,
          value: "empresa"
        },
        {
          text: "Preço",
          align: "start",
          sortable: true,
          value: "preco"
        },
        {
          text: "Setor",
          align: "start",
          sortable: true,
          value: "setor.nome"
        },
        {
          text: "Subsetor",
          align: "start",
          sortable: true,
          value: "subsetor.nome"
        }
      ]
    }
}

export default AcaoController