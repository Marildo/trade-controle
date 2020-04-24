<template>
  <div>
    <v-card>
      <v-card-title>
          <h1>Acões</h1>
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Código"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-data-table :headers="fields" :items="acoes" :search="search"></v-data-table>
    </v-card>
  </div>
</template>

<script>
import gql from "graphql-tag";

export default {
  name: "Acoes",

  components: {},

  data() {
    return {
      acoes: [],
         search: '',
         //TODO compensa criar uma funcao para retorna isso?
         fields: [
           {
             text:'Código',
             align:'start',
             sortable:true,
             value: 'codigo'
           },{
             text: 'Empresa',
             align: 'start',
             sortable: false,
             value: 'empresa'
           },{
             text: 'Preço',
             align: 'start',
             sortable: true,
             value: 'preco'
           },{
             text: 'Setor',
             align: 'start',
             sortable: true,
             value: 'setor.nome'
           }
           ,{
             text: 'Subsetor',
             align: 'start',
             sortable: true,
             value: 'subsetor.nome'
           }
         ]

    };
  },

  mounted() {
    this.loadAcoes();
  },

  methods: {
    loadAcoes() {
      this.$api
        .query({
          query: gql`
            {
              acoes {
                codigo
                empresa
                preco
                setor {id nome}
                  subsetor {id nome}
              }
            }
          `
        })
        .then(resp => (this.acoes = resp.data.acoes))
        .catch(err => console.log(err));
    }
  }
};
</script>

<style>
</style>