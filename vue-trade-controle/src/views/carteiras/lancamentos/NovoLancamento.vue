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
        <v-container>
          <v-form ref="form" lazy-validation>
            <v-card-text>
              <v-row>
                <v-col cols="12" sm="6" md="5">
                  <v-currency-field
                    label="Valor"
                    prefix="R$"
                    v-model.number="movimentacao.valor"
                    :rules="[valorRule]"
                    required
                  />
                </v-col>

                <v-col cols="12" sm="6" md="7">
                  <v-text-field
                    label="Descrição"
                    v-model="movimentacao.descricao"
                    :rules="[v => !!v || 'Informe a descrição']"
                    required
                  />
                </v-col>

                <v-col cols="12">
                  <v-select
                    :items="tiposLancamentos"
                    v-model.number="movimentacao.tipo"
                    label="Tipo de Lançamento"
                    item-text="descricao"
                    item-value="key"
                    required
                    :rules="[v => !!v || 'Selecione um tipo']"
                  />
                </v-col>

                <v-col cols="12" sm="6" md="5">
                  <v-text-field label="Data" v-model="movimentacao.data" type="date"></v-text-field>
                </v-col>

                <v-col cols="12" sm="6" md="5">
                  <v-text-field label="Hora" v-model="movimentacao.hora" type="time"></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
          </v-form>
        </v-container>
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
import { saveLancamento } from "@/controllers/lancamentoController";
import { localDateToYYYMMdd } from "@/lib/dateUtils";
import { mapGetters } from "vuex";


export default {
  name: "NovoLancamento",
  props: ["carteira"],

  data() {
    return {
      dialog: false,
      movimentacao: {},
      valorRule: v =>
        (!!v && parseFloat(v.replace(",", ".")) >= 0.05) ||
        "Valor deve ser maior 0,05"
    };
  },

  computed: {
          ...mapGetters(["tiposLancamentos"])
  },

  mounted() {
    this.resetMovimentacoes();
  },

  methods: {
    salvarLancamento() {
      if (!this.$refs.form.validate()) return;

      const dados = {
        tipo: this.movimentacao.tipo,
        valor: this.movimentacao.valor,
        descricao: this.movimentacao.descricao,
        idCarteira: parseInt(this.carteira.id),
        dataMovimentacao:
          "" +
          new Date(
            this.movimentacao.data + " " + this.movimentacao.hora
          ).getTime()
      };

      saveLancamento(dados).then(() => {
        this.dialog = false;
        this.$refs.form.resetValidation();
        this.resetMovimentacoes();
      });
    },

    resetMovimentacoes() {
      this.movimentacao = {
        data: localDateToYYYMMdd(new Date()),
        hora: new Date().toLocaleTimeString()
      };
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