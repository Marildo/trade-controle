<template>
  <div>
    <div class="row">
      <Trade :carteira="carteira" :isComprar="true" class="btn" />
      <Trade :carteira="carteira" :isComprar="false" class="btn" />
      <NovoLancamento :carteira="carteira" class="btn" />
    </div>

    <div class="row my-5">
      <v-data-table title="Lançamentos" :headers="fields" :items="lancamentos">
        <template v-slot:item.id="{ item }">
          <v-btn small fab color="red darken-2" @click="deleteItem(item)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </div>
  </div>
</template>

<script>
import NovoLancamento from "./NovoLancamento";
import Trade from "./Trade";
import {
  loadLancamentos,
  deleteLancamento
} from "@/controllers/lancamentoController";

import { mapGetters } from "vuex";

export default {
  name: "Lancamentos",
  props: ["carteira"],
  components: {
    NovoLancamento,
    Trade
  },

  mounted() {
    loadLancamentos(this.carteira.id);
  },

  data() {
    return {
      ctrl: {},
      lastLancamento: {},
      fields: [
        { text: "Data", value: "dataMovimentacao" },
        { text: "Valor", value: "valor" },
        { text: "Descrição", value: "descricao" },
        { text: "Tipo", value: "tipoLancamento.descricao" },
        { text: "Excluir", value: "id", sorted: false }
      ]
    };
  },

  computed: {
    ...mapGetters({
      lancamentos: "lancamentos"
    })
  },

  methods: {
    deleteItem(item) {
      deleteLancamento(item)
    }
  }
};
</script>

<style>
</style>