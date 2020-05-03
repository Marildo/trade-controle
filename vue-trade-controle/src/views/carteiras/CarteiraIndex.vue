<template>
  <div>
    <div class="row">
      <v-spacer></v-spacer>
      <v-btn color="secondary" fab x-small dark @click="loadCarteiras">
        <v-icon>mdi-reload</v-icon>
      </v-btn>
      <v-btn color="secondary" fab x-small dark @click.stop="dialog = true">
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </div>

    <table>
      <caption>Carteiras</caption>
      <thead>
        <td>Carteira</td>
        <td>Total Ações</td>
        <td>Total em Caixa</td>
        <td>Último Resultado</td>
        <td>Patrimônio total</td>
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
          <td>R$ 100,00</td>
          <td>R$ 100,00</td>
          <td>R$ {{cdcarteira.saldoCaixa}}</td>
          <td>R$ 100,00</td>
        </tr>
        <tr></tr>
      </tbody>
      <tfoot>
        <td></td>
        <td>
          <h5>R$ 1.000,00</h5>
        </td>
        <td>
          <h5>R$ 1.000,00</h5>
        </td>
        <td>
          <h5>R$ 100,00</h5>
        </td>
        <td>
          <h5>R$ 500,00</h5>
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
  </div>
</template>

<script>
import CarteiraController from "@/controllers/carteiraController";

export default {
  name: "CarteiraIndex",

  data() {
    return {
      carteiras: [],
      dialog: false,
      novaCarteira: ""
    };
  },

  mounted() {
    this.ctrl = new CarteiraController();
    this.loadCarteiras();
  },

  methods: {
    loadCarteiras() {
      this.ctrl
        .findAll()
        .then(resp => (this.carteiras = resp))
        .catch(e => console.log(e.networkError.result.errors));
    },

    salvarCarteira() {
      this.ctrl
        .save(this.novaCarteira)
        .then(resp => {
          this.carteiras.push(resp.data.saveCarteira);
          this.novaCarteira = "";
          this.dialog = false;
        })
        .catch(e => console.log(e.networkError.result.errors));
    }
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