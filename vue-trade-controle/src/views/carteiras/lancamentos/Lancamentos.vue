<template>
  <div>
    <div class="row">
      <Trade :isComprar="true" @inserted="onInserted($event)" class="btn" />

      <Trade :isComprar="false" @inserted="onInserted($event)" class="btn" />

      <NovoLancamento :carteira="carteira" @inserted="onInserted($event)" class="btn" />
    </div>

    <div class="row my-5">
      <v-data-table title="Lançamentos" :headers="fields" :items="lancamentos" />
    </div>
  </div>
</template>

<script>
import NovoLancamento from "./NovoLancamento";
import Trade from "./Trade";
import LancamentoController from "@/controllers/lancamentoController";

import { findAllTipos } from "@/controllers/tiposLancamentosController";
import { formateReal } from "@/lib/numberUtils";

export default {
  name: "Lancamentos",
  props: ["carteira"],
  components: {
    NovoLancamento,
    Trade
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
      fields: [
        { text: "Data", value: "dataMovimentacao", sorted: true },
        { text: "Valor", value: "valor" },
        { text: "Descrição", value: "descricao" },
        { text: "Tipo", value: "tipoLancamento.descricao" }
      ]
    };
  },

  methods: {
    loadLancamentos() {
      this.ctrl
        .findByCarteiraId(this.carteira.id)
        .then(resp => this.formateLancamentos(resp))
        .catch(error => console.log(error));
    },

    formateLancamentos(resp) {
      const formater = item => {
        return {
          ...item,
          valor: formateReal(item.valor),
          dataMovimentacao: new Date(
            parseInt(item.dataMovimentacao)
          ).toLocaleString()
        };
      };
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
      this.$emit("modified", true);
      this.lancamentos.push(inserted);
      this.formateLancamentos(this.lancamentos);
    }
  }
};
</script>

<style>

</style>