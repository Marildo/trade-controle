<template>
  <v-col class="col-12">
    <v-card flat>
      <v-toolbar dense>
        <v-icon>mdi-wallet</v-icon>

        <v-toolbar-title class="mx-2">Carteiras</v-toolbar-title>

        <v-spacer></v-spacer>

        <Trade :isComprar="true"  class="btn" />
        <Trade :isComprar="false" class="btn" />

        <v-btn color="secondary" fab x-small dark @click.stop="dialog = true">
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-toolbar>
    </v-card>

    <table>
      <caption></caption>
      <thead>
        <td>Carteira</td>
        <td>Total Ações</td>
        <td>Total em Caixa</td>
        <td>Último Resultado</td>
        <td>Total Carteira</td>
      </thead>
      <tbody>
        <tr v-for="carteira in carteiras" :key="carteira.id">
          <td>
            <router-link
              :to="{
                name:'Carteira', 
                params:{id: carteira.id}
            }"
            >{{carteira.nome}}</router-link>
          </td>
          <td>R$ {{carteira.saldoAcoes | formaterReal}} </td>
          <td>R$ {{carteira.saldoCaixa | formaterReal}}</td>
          <td>R$ 100,33</td>
          <td>R$ {{carteira.saldoCaixa + carteira.saldoAcoes | formaterReal}}</td>
        </tr>
        <tr></tr>
      </tbody>
      <tfoot>
        <td></td>
        <td>
          <h5  class="saldo"> {{patrimonio.totalAcoes | formaterReal}}</h5>
        </td>
        <td>
          <h5  class="saldo"> {{patrimonio.totalCaixa | formaterReal}}</h5>
        </td>
        <td>
          <h5 class="saldo">R$ 100,00</h5>
        </td>
        <td>
          <h5 class="saldo"> {{patrimonio.total | formaterReal}}</h5>
        </td>
      </tfoot>
    </table>

    <v-dialog v-model="dialog" max-width="290">
      <v-card>
        <v-card-title class="headline">Nova Carteira</v-card-title>
        <v-spacer></v-spacer>

        <v-card-text>
          <v-row>
            <v-text-field label="Nome" v-model="novaCarteira" required></v-text-field>
            <br />
          </v-row>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="orange darken-1" @click="dialog = false">Cancelar</v-btn>
          <v-btn color="green darken-1" @click="salvarCarteira">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-col>
</template>

<script>
import Trade from "./lancamentos/Trade";

import {saveCarteira} from "@/controllers/carteiraController";
import { mapGetters } from "vuex";

export default {
  name: "CarteiraIndex",

  components: {
    Trade
  },

  data() {
    return {
      dialog: false,
      novaCarteira: ""
    };
  },

  mounted() {},

  computed: {
    ...mapGetters(["carteiras","patrimonio"]),
  },

  methods: {
    carteiraSelected() {
      return this.carteiras[0];
    },

    salvarCarteira() {
        saveCarteira(this.novaCarteira)
        .then(() => {
          this.novaCarteira = "";
          this.dialog = false;
        })       
    },
  }
};
</script>

<style>
td {
  padding: 22px;
  border: 1px solid white;
  border-spacing: 5px;
}
</style>