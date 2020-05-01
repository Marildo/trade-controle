<template>
  <div>
    <v-toolbar>
      <v-toolbar-title>Carteira: {{carteira.nome}}</v-toolbar-title>
      <template v-slot:extension>
        <v-tabs v-model="tab" align-with-title>
          <v-tabs-slider color="yellow"></v-tabs-slider>
          <v-tab>Patrimônio</v-tab>
          <v-tab>Ações</v-tab>
          <v-tab>Lançamentos</v-tab>
        </v-tabs>
      </template>
    </v-toolbar>

    <div class="conteudo">
      <v-tabs-items v-model="tab">
        <v-tab-item>
          <div class="row">
            <div class="card">
              <h4>Total Ações</h4>
              <h5>R$ 190,00</h5>
            </div>

            <div class="card">
              <h4>Total em Caixa</h4>
              <h5>R$ 190,00</h5>
            </div>

            <div class="card">
              <h4>Patrimônio Total</h4>
              <h5>R$ 190,00</h5>
            </div>

            <div class="card">
              <h4>Resultado Mensal</h4>
              <h5>R$ 190,00</h5>
            </div>
            <div class="card">
              <h4>Resultado Semanal</h4>
              <h5>R$ 190,00</h5>
            </div>
            <div class="card">
              <h4>Ultimo Resultao</h4>
              <h5>R$ 190,00</h5>
            </div>
          </div>
        </v-tab-item>

        <v-tab-item>
          <div class="row">tabela de acoes</div>
        </v-tab-item>

        <v-tab-item>
          <div class="row">
            <v-btn color="teal" class="btn">
              <v-icon>mdi-cart-plus</v-icon>Comprar
            </v-btn>
            <v-btn color="deep-orange darken-4" class="btn">
              <v-icon>mdi-cart-off</v-icon>Vender
            </v-btn>
            <v-btn color="blue darken-3" class="btn">
              <v-icon>mdi-contrast-box</v-icon>Lançamentos
            </v-btn>
          </div>
        </v-tab-item>
      </v-tabs-items>
    </div>
  </div>
</template>

<script>
import CarteiraController from "@/controllers/carteiraController";

export default {
  props: ["id"],

  components: {},

  data() {
    return {
      carteira: {},
      tab: null,
      items: ["Patrimônio", "Ações", "Lançamentos", "images", "news"]
    };
  },

  mounted() {
    this.ctrl = new CarteiraController();
    this.loadCarteira();
  },

  methods: {
    loadCarteira() {
      this.ctrl
        .findById(this.id)
        .then(resp => (this.carteira = resp.data.carteira))
        .catch(error => console.log(error));
    }
  }
};
</script>

<style scope>
.card {
  margin: 10px 10px 0 0;
  padding: 10px;
  border: 1px solid snow;
  height: 60px;
  width: 300px;
  text-align: center;
}

.card h5 {
  color: yellowgreen;
}

.conteudo {
  width: 100%;
  margin: 15px;
}

.btn {
  margin-right: 10px;
}
</style>