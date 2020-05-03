<template>
  <div>
    <v-toolbar>
      <v-toolbar-title>Carteira: {{carteira.nome}}</v-toolbar-title>
      <v-spacer></v-spacer>
      <span class="saldo">
        <v-icon large color="amber lighten-2">fa-university</v-icon>
        Saldo: {{carteira.saldoCaixa | formateReal}}
      </span>

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
              <h5>{{carteira.saldoAcoes| formateReal}}</h5>
            </div>

            <div class="card">
              <h4>Total em Caixa</h4>
              <h5>{{carteira.saldoCaixa | formateReal}}</h5>
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
          <AcoesCarteira />
        </v-tab-item>

        <v-tab-item>
          <Lancamentos :carteira="carteira" @modified="onModified($event)" />
        </v-tab-item>
      </v-tabs-items>
    </div>
  </div>
</template>

<script>
import AcoesCarteira from "./AcoesCarteira";
import Lancamentos from "./lancamentos/Lancamentos";

import CarteiraController  from '@/controllers/carteiraController'

import { mapGetters } from "vuex";

export default {
  props: ["id"],

  components: {
    AcoesCarteira,
    Lancamentos
  },

  computed: {
    ...mapGetters({
      carteira: "getCarteira"
    })
  },

  data() {
    return {
      tab: null
    };
  },

  watch: {},

  mounted() {
    this.$store.dispatch("setCarteira", this.id);
  },

  methods: {
    onModified() {
      new CarteiraController().findById(this.id)
      .then(resp =>{ 
        this.$store.dispatch("updateCarteira", resp.data.carteira)
        console.log('recaregando a carteira:', resp.data.carteira)
      })
      .catch(error => console.log(error))
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

.saldo {
  color: rgb(255, 254, 196);
  display: inline;
}

.conteudo {
  width: 100%;
  margin: 15px;
}
</style>