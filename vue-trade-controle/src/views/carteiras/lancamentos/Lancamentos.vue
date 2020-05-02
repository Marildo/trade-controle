<template>
  <div>
    Modificado:{{modified}}
    <div class="row">
      <v-btn color="teal" class="btn">
        <v-icon>mdi-cart-plus</v-icon>Comprar
      </v-btn>
      <v-btn color="deep-orange darken-4" class="btn">
        <v-icon>mdi-cart-off</v-icon>Vender
      </v-btn>
      <NovoLancamento :carteira="carteira" @inserted="onInserted($event)" class="btn" />
    </div>

    <div class="row my-5">
      <v-data-table :headers="fields" :items="lancamentos">
        <template v-slot:item.dataMovimentacao="{ item }">
          <span>{{new Date(parseInt(item.dataMovimentacao)).toLocaleString()}}</span>
        </template>
        <template v-slot:item.valor="{ item }">
          <span>
            {{item.valor.toLocaleString('pt-BR', {
            style: 'currency',
            currency: 'BRL',
            })}}
          </span>
        </template>
      </v-data-table>
    </div>
  </div>
</template>

<script>
import NovoLancamento from "./NovoLancamento";
import LancamentoController from "@/controllers/lancamentoController";
import { findAllTipos } from "@/controllers/tiposLancamentosController";

export default {
  name: "Lancamentos",
  props: ["carteira"],
  components: {
    NovoLancamento
  },

  mounted() {
    this.ctrl = new LancamentoController();
    this.loadTiposLancamentos();
    this.loadLancamento();
  },

  updated() {
    this.loadLancamento();
    this.modified= false
  },

  data() {
    return {
      modified: false,
      ctrl: {},
      lancamentos: [],
      fields: [
        { text: "Data", value: "dataMovimentacao", sorted: true },
        { text: "Valor", value: "valor" },
        { text: "Descrição", value: "descricao" },
        { text: "Tipo", value: "tipo" }
      ]
    };
  },

  methods: {
    loadLancamento() {
      this.ctrl
        .findByCarteiraId(null)
        .then(resp => {
          this.lancamentos = resp;
          console.log("carregando:", this.lancamentos.length);
        })
        .catch(error => console.log(error));
    },

    loadTiposLancamentos() {
      const tipos = this.$store.getters.tiposLancamentos;
      if (tipos.length == 0) {
        findAllTipos()
          .then(resp =>
            this.$store.commit(
              "setTiposLancamentos",
              resp.data.tiposLancamentos
            )
          )
          .catch(error => console.log(error));
      }
    },

    onInserted(inserted) {
      this.modified = inserted;
    }
  }
};
</script>

<style>
    .btn {
      margin-right: 10px;
    }
</style>