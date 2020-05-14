<template>
  <div>
    <v-btn
      class="btn"
      @click.stop="showForm"
      width="120"
      :color="isComprar ? 'teal' : 'deep-orange darken-4'"
    >
      <v-icon>{{icon()}}</v-icon>
      {{isComprar ? "Comprar" : "Vender"}}
    </v-btn>

    <v-dialog v-model="dialog" persistent max-width="550px">
      <v-card style="border: 1px solid snow;">
        <v-card-title class="headline col-12">
          <div :class="styleTitle">
            <v-icon :class="styleTitle">{{icon()}}</v-icon>
            {{isComprar ? "Compra" : "Venda"}} de Ações
            <hr />
          </div>
        </v-card-title>
        <v-container>
          <v-form ref="form" lazy-validation>
            <v-card-text>
              <v-row>
                <v-col cols="12" sm="6" md="6">
                  <v-select
                    label="Carteira"
                    :items="carteiras"
                    item-value="id"
                    item-text="nome"
                    v-model="form.idCarteira"
                    required
                    :rules="[carteiraIdRule]"
                  />
                </v-col>

                <v-col cols="12" sm="6" md="6">
                  <v-select
                    :items="acoes"
                    v-model="form.acao"
                    label="Ação"
                    item-value="acao"
                    required
                    :rules="[v => !!v || 'Seleciona uma ação']"
                  />
                </v-col>

                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="Quantidade"
                    type="number"
                    v-model.number="form.quantidade"
                    :rules="[quantidadeRule]"
                    required
                  />
                </v-col>

                <v-col cols="12" sm="6" md="4">
                  <v-currency-field
                    label="Valor"
                    prefix="R$"
                    v-model.number="form.valor"
                    :rules="[valorRule]"
                    required
                  />
                </v-col>

                <v-col cols="12" sm="6" md="4">
                  <v-currency-field
                    label="Corretagem"
                    prefix="R$"
                    v-model.number="form.corretagem"
                    required
                  />
                </v-col>

                <v-col cols="12" sm="6" md="4">
                  <v-currency-field
                    label="Impostos"
                    prefix="R$"
                    v-model.number="form.impostos"
                    required
                  />
                </v-col>

                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="Data"
                    v-model="form.data"
                    type="date"
                    required
                    :rules="[dataRule]"
                  />
                </v-col>

                <v-col cols="12" sm="6" md="4">
                  <v-text-field label="Hora" v-model="form.hora" type="time" required></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
          </v-form>
        </v-container>
        <!-- TODO criar um componente para esse botoes-->
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="orange darken-1" @click="dialog = false">Cancelar</v-btn>
          <v-btn color="green darken-1" @click="salvar">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { localDateToYYYMMdd } from "@/lib/dateUtils";
import { showToastSuccess, showToastError } from "@/lib/messages";
import { saveTrade } from "@/controllers/tradeController";

export default {
  name: "Trade",
  props: ["carteira", "isComprar"],

  data() {
    return {
      dialog: false,
      form: {},

      icon: () => (this.isComprar ? "mdi-cart-plus" : "mdi-cart-off"),

      // TODO colocar validacoes em um MIXIN
      valorRule: v =>
        (!!v && parseFloat(v.replace(",", ".")) >= 0.05) ||
        "Valor deve ser maior 0,05",

      quantidadeRule: v => (!!v && parseInt(v) > 0) || "Informe a quantidade",

      dataRule: v => (!!v && !isNaN(Date.parse(v))) || "Informe a data",

      carteiraIdRule: v => (!!v && parseInt(v) > 0) || "Selecione uma Carteira"
    };
  },

  mounted() {
   
  },

  computed: {
    acoes() {
      return this.$store.getters.acoes.map(a => {
        return {
          text: `${a.codigo} - ${a.empresa}`,
          acao: {
            id: `${a.id}`,
            codigo: `${a.codigo}`
          }
        };
      });
    },

    carteiras() {
      return this.$store.getters.carteiras;
    },

    styleTitle() {
      return {
        titleCompra: this.isComprar,
        titleVenda: !this.isComprar
      };
    }
  },

  methods: {
    salvar() {
      if (!this.$refs.form.validate()) return;

      saveTrade(this.form)
        .then(resp => {
          this.dialog = false;
          this.$refs.form.resetValidation();
          this.resetFields();
          this.$emit("inserted", resp.data.saveTradeAcao);
          showToastSuccess();
        })
        .catch(e => {
          console.log(e);
          console.log(e.networkError.result);
          showToastError(e.networkError.result.errors[0].message);
        });
    },

    resetFields() {
      this.form = {
        data: localDateToYYYMMdd(new Date()),
        hora: new Date().toLocaleTimeString(),
        quantidade: 0,
        compraf: this.isComprar,
        compra: true
      };

      if (this.carteira) this.form.idCarteira = this.carteira.id;
    },

    showForm() {
      this.dialog = true;
      this.resetFields();
    }
  }
};
</script>

<style scoped>
.btn {
  margin-right: 5px;
}
.titleCompra {
  color: teal;
}

.titleVenda {
  color: #bf3600;
}
</style>