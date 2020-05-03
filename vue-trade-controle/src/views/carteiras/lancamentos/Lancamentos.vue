<template>
  <div>
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
      <v-data-table title="Lançamentos" :headers="fields" :items="lancamentos" />
    </div>
  </div>
</template>

<script>
import NovoLancamento from "./NovoLancamento";
import LancamentoController from "@/controllers/lancamentoController";
import { findAllTipos } from "@/controllers/tiposLancamentosController";
import {formateReal} from '@/lib/numberUtils'

export default {
  name: "Lancamentos",
  props: ["carteira"],
  components: {
    NovoLancamento
  },

  mounted() {
    this.ctrl = new LancamentoController();
    this.loadTiposLancamentos();
    this.loadLancamentos();
  },

  data() {
    return {
      ctrl: {},
      lancamentos: [],
      lastLancamento: {},
      modified: false,
      fields: [
        { text: "Data", value: "dataMovimentacao", sorted: true },
        { text: "Valor", value: "valor" },
        { text: "Descrição", value: "descricao" },
        { text: "Tipo", value: "tipoLancamento.descricao" }
      ]
    };
  },

  watch: {
    modified() {
      this.loadLancamentos();
    }
  },

  methods: {
    loadLancamentos() {
      this.ctrl
        .findByCarteiraId(this.carteira.id)
        .then(resp => this.formateLancamentos(resp))
        .catch(error => console.log(error));
    },

    formateLancamentos(resp) {
      console.log("carregando:", resp.length);

     const formater = (item) => {
       return {
         ...item,
         valor: formateReal(item.valor),
         dataMovimentacao: new Date(parseInt(item.dataMovimentacao)).toLocaleString()
       }
     }

      this.lancamentos = resp.map(formater);
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