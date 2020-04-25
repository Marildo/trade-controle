<template>
  <div>
    <!--TODO criar um component para headers das paginas -->
    <v-card color="grey lighten-4" flat height="60px" tile>
      <v-toolbar extended extension-height="20">
        <v-toolbar-title>Açoes</v-toolbar-title>
        <v-spacer></v-spacer>

        <v-text-field
          v-model="search"
          prepend-icon="mdi-filter"
          label="Pesquisa"
          single-line
          hide-details
          wid
        ></v-text-field>
        <v-btn color="secondary" fab x-small dark @click="clearSearch">
          <v-icon>mdi-filter-remove</v-icon>
        </v-btn>
        <v-spacer></v-spacer>

        <v-col cols="6" sm="3">
          <v-text-field 
          v-model="novaAcao" 
          prepend-icon="mdi-plus"
          label="Nova Ação" 
          single-line 
          hide-details>
          </v-text-field>
        </v-col>

        <div class="my-2">
          <v-btn color="secondary" fab x-small dark @click="salvaAcao">
            <v-icon>mdi-content-save</v-icon>
          </v-btn>
        </div>
      </v-toolbar>
    </v-card>

    <v-card>
      <!--TODO criar um component de tabela prorio -->
      <v-data-table :headers="fields" :items="acoes" :search="search"></v-data-table>
    </v-card>
  </div>
</template>

<script>
import gql from "graphql-tag";

export default {
  name: "Acoes",

  data() {
    return {
      dialog: false,
      acoes: [],
      search: "",
      novaAcao: "",

      //TODO compensa criar uma funcao para retorna isso?
      fields: [
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
    };
  },

  mounted() {
    this.loadAcoes();
  },

  methods: {
    clearSearch() {
      this.search = "";
    },

    //TODO passar metodos para um controller
    loadAcoes() {
      this.$api
        .query({
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
        })
        .then(resp => (this.acoes = resp.data.acoes))
        .catch(err => console.log(err));
    },

    salvaAcao() {
      //TODO alterar metodo para trazer acao completa na mutatio evitando novo requeste
      this.$api
        .mutate({
          mutation: gql`
            mutation($codigo: String!) {
              newAcao(codigo: $codigo) {
                id
                codigo
              }
            }
          `,
          variables: {
            codigo: this.novaAcao
          }
        })
        .then(resp => {
          this.loadAcao(resp.data.newAcao.codigo);
          this.$toast.add({
            severity: "success",
            summary: "Informação",
            detail: this.novaAcao + " Adicionado com sucesso",
            life: 3000
          });
        })
        .catch(e => {
           console.log(e);
          // console.log(e.networkError.result.errors)
          this.$toast.add({
            severity: "error",
            summary: "Falha ao inserir " + this.novaAcao,
            detail: e.message.replace('GraphQL error:',''),
            life: 6000
          })
        })
    },

    loadAcao(_codigo) {
      this.$api
        .query({
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
            codigo: _codigo
          }
        })
        .then(resp => {
          const acao = resp.data.acao;
          if (!this.acoes.includes(acao)) {
            this.acoes.push(acao);
          }
          this.newAcao = null
        })
        .catch(e => console.log(e.networkError.result.errors))
    }
  }
}
</script>

<style>
</style>