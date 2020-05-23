<template>
  <div class="contaneir">
    <div class="row my-5">
      <v-data-table title="Portifólio de açoes" :headers="fields" :items="portifolio">
      </v-data-table>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "Portifolio",
  props: ["id"],

  computed: {
    ...mapGetters(['portifolio']),
  },

    data() {
    return {
      fields: [
        { text: "Codigo", value: "codigoAcao" },
        { text: "Última", value: "cotacao" },
        { text: "Quantidade", value: "quantidade" },
        { text: "Valor Atual", value: "totalAtual" },
        { text: "Custo Total", value: "custoTotal" },
        { text: "Resultado", value: "resultado" },
        { text: "%", value: "percentual" }
      ]
    };
  },

};
</script>

<style>
</style>