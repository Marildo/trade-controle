<template>
  <div>
    <div class="row">
      <Trade :carteira="carteira" :isComprar="true" @inserted="onInserted($event)" class="btn" />

      <Trade :carteira="carteira" :isComprar="false" @inserted="onInserted($event)" class="btn" />

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


import { mapGetters } from "vuex";

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
      lastLancamento: {},
      fields: [
        { text: "Data", value: "dataMovimentacao", sorted: true },
        { text: "Valor", value: "valor" },
        { text: "Descrição", value: "descricao" },
        { text: "Tipo", value: "tipoLancamento.descricao" }
      ]
    };
  },


  computed:{
    ...mapGetters({
      lancamentos: "lancamentos"
    })
  },

  methods: {    
    loadLancamentos() {
      this.ctrl
        .loadLancamentos(this.carteira.id)
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
      this.$store.dispatch("addLancamento",inserted)
    }
  }
};
</script>

<style>

</style>