<template>
  <div >
    <q-btn flat :color = "isBuy ? 'green' : 'red'"
       icon="fas fa-shopping-cart"
       @click="showForm = true"
    />

    <q-dialog v-model="showForm" persistent>
      <q-card>
        <q-card-section>
          <q-avatar icon="fas fa-shopping-cart" :color = "isBuy ? 'green' : 'red'" text-color="white" />
          <span class="q-ml-sm text-subtitle1 text-blue-grey-9">{{ isBuy ? "Compra" : "Venda"}} de ações</span>
        </q-card-section>

        <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md" >
          <q-card-actions class="row q-pa-md" align="center">
              <q-input class="q-ma-sm col-md-3 col-5"
                filled
                v-model="trade.carteira.nome"
                label="Carteira"
                :readonly=true
                 :rules="['']"
              />

              <q-select class="q-ma-sm col-md-3 col-5"
                filled
                label ="Ação *"
                v-model="trade.acao"
                use-input
                hide-selected
                fill-input
                input-debounce="0"
                :options="acoes"
                option-label="codigo"
                @filter="filterCodigo"
                lazy-rules
                :rules="[
                 val => val !== null && val !== '' || 'Selecione uma ação'
                ]"
               >
               <template v-slot:no-option>
                 <q-item>
                  <q-item-section class="text-grey">
                    Código não localizado
                  </q-item-section>
                 </q-item>
               </template>
              </q-select>

               <q-input class="q-ma-sm col-md-3 col-5"
                filled
                type="number"
                v-model="trade.quantidade"
                label="Quantidade *"
                lazy-rules
                :rules="quantidadeRule"
              />

             <q-field class="q-ma-sm col-md-3 col-5"
              filled
              v-model="trade.valor"
              label="Valor *"
              prefix= 'R$ '
              lazy-rules
              :rules="[
                 val => val !== null && val !== '' || 'Please type your age',
                 val => val > 0  || 'Please type a real age'
               ]"
              >
              <template v-slot:control="{ id, floatingLabel, value, emitValue }">
                <input :id="id" class="q-field__input text-right"
                  :value="value"
                  @change="e => emitValue(e.target.value)"
                  v-money="moneyFormatForDirective"
                  v-show="floatingLabel"
                >
              </template>
              <q-tooltip >
                {{ trade.acao.preco }}
              </q-tooltip>
             </q-field>

             <q-field class="q-ma-sm col-md-3 col-5"
              filled
              v-model="trade.corretagem"
              label="Corretagem "
              prefix= 'R$ '
              lazy-rules
              :rules="[
                 val => val !== null && val !== '' || 'Please type your age',
                 val => val > 0  || 'Please type a real age'
               ]"
              >
              <template v-slot:control="{ id, floatingLabel, value, emitValue }">
                <input :id="id" class="q-field__input text-right"
                  :value="value"
                  @change="e => emitValue(e.target.value)"
                  v-money="moneyFormatForDirective"
                  v-show="floatingLabel"
                >
              </template>
              <q-tooltip >
                 sugestão
              </q-tooltip>
             </q-field>

             <q-field class="q-ma-sm col-md-3 col-5"
              filled
              v-model="trade.impostos"
              label="Impostos "
              prefix= 'R$ '
              lazy-rules
              :rules="[
                 val => val !== null && val !== '' || 'Please type your age',
                 val => val > 0  || 'Please type a real age'
               ]"
              >
              <template v-slot:control="{ id, floatingLabel, value, emitValue }">
                <input :id="id" class="q-field__input text-right"
                  :value="value"
                  @change="e => emitValue(e.target.value)"
                  v-money="moneyFormatForDirective"
                  v-show="floatingLabel"
                >
              </template>
              <q-tooltip >
                 sugestão
              </q-tooltip>
             </q-field>

            </q-card-actions>
            <q-card-actions align="right" class="row bg-blue-grey-14 shadow-box shadow-3">
              <q-btn label="Cancelar" type="reset" color="negative" class="q-ma-3 col-md-2 col-12" />
              <q-btn label="Salvar"  type="submit" color="positive" class="q-ma-3 col-md-2 col-12" />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>
  </div>

</template>

<script>
import { VMoney } from 'v-money'

export default {
  name: 'Trade',

  props: ['carteira', 'isBuy'],

  data () {
    return {
      showForm: false,

      acoes: [],

      trade: {
        carteira: this.carteira,
        acao: { codigo: '', preco: '' },
        quantidade: ''
      },

      moneyFormatForDirective: {
        decimal: ',',
        thousands: '.',
        precision: 2,
        masked: false /* doesn't work with directive */
      },

      quantidadeRule: [v => (!!v && parseInt(v) > 0) || 'Informe a quantidade']
    }
  },

  mounted () {
    this.acoes = this.$store.state.acoes.all
  },

  methods: {
    onReset () {
      this.showForm = false
    },

    onSubmit () {
      console.log(this.trade)
    },

    filterCodigo (val, update) {
      update(() => {
        const all = this.$store.state.acoes.all
        this.acoes = all.slice(0, all.length)
          .filter(v => v.codigo.indexOf(val.toUpperCase()) > -1)
      })
    }
  },
  directives: { money: VMoney }
}
</script>

<style scoped>
  .mg {
    margin: 0.1em;
  }
</style>
