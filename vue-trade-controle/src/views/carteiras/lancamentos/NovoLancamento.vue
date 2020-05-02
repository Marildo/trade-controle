<template>
  <div>
    <v-btn color="blue darken-3" class="btn" @click.stop="dialog = true">
      <v-icon>mdi-contrast-box</v-icon>Novo Lançamento
    </v-btn>

    <v-dialog v-model="dialog" persistent max-width="500px">
      <v-card style="border: 1px solid snow;">
        <v-card-title class="headline">
          Novo Lançamento em
          <span class="carteira">{{carteira.nome}}</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" sm="6" md="5">
                <v-currency-field label="Valor" prefix="R$" v-model="movimentacao.valor" />
              </v-col>

              <v-col cols="12" sm="6" md="7">
                <v-text-field label="Descrição" v-model="movimentacao.descricao" required></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-select
                  :items="tiposLancamentos"
                  v-model="movimentacao.tipo"
                  label="Tipo de Lançamento"
                  item-text="tipo"
                  item-value="key"
                />
              </v-col>

              <v-col cols="12" sm="6" md="5">
                <v-text-field label="Data" v-model="movimentacao.data" type="date"></v-text-field>
              </v-col>

              <v-col cols="12" sm="6" md="5">
                <v-text-field label="Hora" v-model="movimentacao.hora" type="time"></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="orange darken-1" @click="dialog = false">Cancelar</v-btn>
          <v-btn color="green darken-1" @click="salvarLancamento">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import LancamentoController from "@/controllers/lancamentoController";
import { localDateToYYYMMdd } from "@/lib/dateUtils";
import { showToastSuccess, showToastError } from "@/lib/messages";

export default {
  name: "NovoLancamento",
  props: ["carteira"],
  data() {
    return {
      dialog: false,
      movimentacao: {
        data: localDateToYYYMMdd(new Date()),
        hora: new Date().toLocaleTimeString()
      },
      tiposLancamentos: [
        { key: 0, tipo: "Aporte" },
        { key: 1, tipo: "Retirada" }
      ]
    };
  },

  methods: {
    salvarLancamento() {
      const dados = {
        tipo: parseInt(this.movimentacao.tipo),
        valor: parseFloat(this.movimentacao.valor),
        descricao: this.movimentacao.descricao,
        idCarteira: parseInt(this.carteira.id),
        dataMovimentacao:
          new Date(
            this.movimentacao.data + " " + this.movimentacao.hora
          ).getTime() + ""
      };

      const ctrl = new LancamentoController();
      ctrl
        .save(dados)
        .then(() => {
          this.dialog = false;
          showToastSuccess();
        })
        .catch(e => {
          console.log(e, e.networkError.result.errors);
          showToastError(e.networkError.result.errors[0]);
        });
    }
  }
};
</script>

<style scoped>
.carteira {
  color: goldenrod;
  margin-left: 0.3em;
}
</style>