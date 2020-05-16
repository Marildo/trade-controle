import gql from 'graphql-tag'
import vue from 'vue'

// TODO deixar gql em arquivos separados
// TODO usar fragmentos

const ctrlLoadAcoes = () => {
  return vue.prototype.$api.query({
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
}

const ctrlSaveAcao = (codigo) => {
  return new Promise((resolve, reject) => {
    vue.prototype.$api.mutate({
      mutation: gql`
          mutation($codigo: String!) {
            newAcao(codigo: $codigo) {
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
    })
      .then(resp => resolve(resp.data.newAcao))
      .catch(error => reject(error))
  })
}

const ctrlFindAcaoByCodigo = (codigo) => {
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
}

export {
  ctrlLoadAcoes,
  ctrlFindAcaoByCodigo,
  ctrlSaveAcao
}