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
import LancamentoController from "@/controllers/lancamentoController";
import { localDateToYYYMMdd } from "@/lib/dateUtils";
import { showToastSuccess, showToastError } from "@/lib/messages"
import {formateReal} from '@/lib/numberUtils'

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
    tiposLancamentos() {
      const tipos = this.$store.getters.tiposLancamentos;
      return tipos.filter(t => parseInt(t.key) >= 2);
    }
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

      const ctrl = new LancamentoController();
      ctrl
        .save(dados)
        .then(() => {
          this.dialog = false;
          this.$emit("inserted",true);
          this.$refs.form.resetValidation()
          this.resetMovimentacoes()
          showToastSuccess(dados.descricao+ ' no valor de '+formateReal(dados.valor) + ' foi inserido');
        })
        .catch(e => {
          console.log(e);
          console.log(e.networkError.result);
          showToastError(e.networkError.result.errors[0].message);
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