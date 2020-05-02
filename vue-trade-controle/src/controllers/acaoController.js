import gql from 'graphql-tag'
import vue from 'vue'

function AcaoController() {
  this.findAll = function () {
    return vue.prototype.$api.query({
      query: gql`
            {
              acoes {
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
    });
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