import gql from 'graphql-tag'
import vue from 'vue'

import store from '@/store';
import { showToastSuccess, catchError } from '@/lib/messages'



// TODO deixar gql em arquivos separados
// TODO usar fragmentos

const loadAcoes = () => {
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
    .then(resp => resp.data.acoes)
    .then(acoes => store.commit('acoes', acoes))
    .catch(error => catchError(error))
}

const saveAcao = (codigo) => {
  return new Promise((resolve, reject) => {
    vue.prototype.$api.mutate({
      mutation: gql`
          mutation($codigo: String!) {
            newAcao(codigo: $codigo) {
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
        `,
      variables: {
        codigo
      }
    })
      .then(resp => resp.data.newAcao)
      .then(acao => {
        showToastSuccess(acao.codigo + ' adicionada com sucesso!');
        store.dispatch('addAcao', acao)
        resolve(acao)
      })
      .catch(error => {
        catchError(error)
        reject(false)
      })
  })
}

const findAcaoByCodigo = (codigo) => {
  return new Promise((resolve, reject) => {
    vue.prototype.$api.query({
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
    }).then(resp => resolve(resp.data.acao))
      .catchr(error => reject(error))
  })
}

export {
  loadAcoes,
  findAcaoByCodigo,
  saveAcao
}