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

        <v-btn
          :disabled="search.length < 1"
          color="secondary"
          fab
          x-small
          dark
          @click="clearSearch"
        >
          <v-icon>mdi-filter-remove</v-icon>
        </v-btn>
        <v-spacer></v-spacer>

        <v-col cols="6" sm="3">
          <v-text-field
            v-model="novaAcao"
            prepend-icon="mdi-plus"
            label="Nova Ação"
            single-line
            hide-details
          ></v-text-field>
        </v-col>

        <div class="my-2">
          <v-btn
            :disabled="enableSave()"
            color="secondary"
            fab
            x-small
            dark
            @click="salvaAcao"
          >
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
import { saveAcao } from "@/controllers/acaoController";
import { mapGetters } from "vuex";

export default {
  name: "Acoes",

  data() {
    return {
      dialog: false,
      search: "",
      novaAcao: "",

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

  mounted() {},

  computed: {
    ...mapGetters({
      acoes: "acoes"
    })
  },

  methods: {
    clearSearch() {
      this.search = "";
    },

    enableSave(){
      // TODO fazer validacao co regex
      return !(this.novaAcao.length >= 5) && (this.novaAcao.length <= 6)
    },

    salvaAcao() {
        saveAcao(this.novaAcao) 
        .then((resp) =>{
               this.search = resp.codigo
               this.novaAcao = ""         
             })                 
    },
  }
}
</script>

<style>
</style>