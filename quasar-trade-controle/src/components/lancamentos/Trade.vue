<template>
  <div >
    <q-btn flat :color = "getColor()"
       :icon="getIcon()"
       @click="onShowForm"
    >
      <q-tooltip >
         {{ title() }}
      </q-tooltip>
    </q-btn>

    <q-dialog v-model="showForm" persistent>
      <q-card>
        <q-card-section>
          <q-avatar :icon="getIcon()" :color = "getColor()" text-color="white" />
          <span class="q-ml-sm text-subtitle1 text-blue-grey-9">{{ title() }} de ações</span>
          <hr>
        </q-card-section>

        <q-form class="q-gutter-md"  ref="formTrade" >
          <q-card-actions class="row q-pa-md flex justify-start">
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
                option-label="codigo"
                :options="acoes"
                @filter="filterCodigo"
                lazy-rules
                :rules="acaoRule"
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

             <q-field class="q-ma-sm col-md-3 col-5"  v-show="showFieldCompra()"
              filled
              v-model="trade.precoCompra"
              label="Pr. Compra *"
              prefix= 'R$ '
              lazy-rules
              :rules="compraRule"
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
                Cotação: {{ trade.acao.preco }}
              </q-tooltip>
             </q-field>

              <q-field class="q-ma-sm col-md-3 col-5"  v-show="showFieldVenda()"
              filled
              v-model="trade.precoVenda"
              label="Pr. Venda *"
              prefix= 'R$ '
              lazy-rules
              :rules="vendaRule"
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
                Cotação: {{ trade.acao.preco }}
              </q-tooltip>
             </q-field>

             <q-field class="q-ma-sm col-md-3 col-5"
              filled
              v-model="trade.corretagem"
              label="Corretagem "
              prefix= 'R$ '
              lazy-rules
              :rules="['']"
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
              :rules="['']"
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

             <q-input class="q-ma-sm col-md-6 col-10"
               filled
               v-model="trade.dataTrade"
               label="Data"
               mask="##/##/#### ##:##:##"
              lazy-rules
              :rules="['']"
             >
               <template v-slot:prepend>
                 <q-icon name="event" class="cursor-pointer">
                   <q-popup-proxy transition-show="scale" transition-hide="scale">
                     <q-date v-model="trade.dataTrade" mask="DD/MM/YYYY HH:mm:ss" />
                   </q-popup-proxy>
                 </q-icon>
               </template>
               <template v-slot:append>
                 <q-icon name="access_time" class="cursor-pointer">
                   <q-popup-proxy transition-show="scale" transition-hide="scale">
                     <q-time v-model="trade.dataTrade" mask="DD/MM/YYYY HH:mm:ss" format24h />
                   </q-popup-proxy>
                 </q-icon>
               </template>
             </q-input>
            </q-card-actions>
            <q-card-actions align="right" class="row bg-blue-grey-14 shadow-box shadow-3">
              <q-btn label="Cancelar" @click="onReset" type="button" color="negative" class="mBtn col-md-2 col-12" />
              <q-btn label="Salvar" @click="onSubmit" type="button" color="positive" class="mBtn col-md-2 col-12" />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>
  </div>

</template>

<script>
import { VMoney } from 'v-money'
import { sucessMessage, errorMessage } from '../../utils/message'

export default {
  name: 'Trade',

  props: ['carteira', 'isBuy', 'tipoTrade'],

  data () {
    return {
      showForm: false,
      acoes: [],
      trade: {},

      moneyFormatForDirective: {
        decimal: ',',
        thousands: '.',
        precision: 2,
        masked: false
      },

      quantidadeRule: [v => this.validateQuantidade(v) || 'Informe a quantidade'],
      compraRule: [v => ((!this.showFieldCompra()) || (!!v && v !== '0,00')) || 'Informe o preço de compra'],
      vendaRule: [v => ((!this.showFieldVenda()) || (!!v && v !== '0,00')) || 'Informe o preco de venda'],
      acaoRule: [val => (val && val.codigo.length > 3) || 'Selecione uma ação']
    }
  },

  created () {
    this.acoes = this.$store.state.acoes.all
    this.onReset()
  },

  methods: {
    validateQuantidade (v) {
      return !!v && (v.indexOf(',') + v.indexOf('.') === -2)
    },

    onShowForm () {
      this.onReset()
      this.showForm = true
    },

    onReset () {
      this.showForm = false
      this.trade = {
        precoCompra: 0,
        precoVenda: 0,
        carteira: this.carteira,
        acao: { codigo: '', preco: '0,00' },
        quantidade: 100,
        dataTrade: new Date().toLocaleString()
      }
    },

    onSubmit () {
      // console.trace(this.trade)
      this.$refs.formTrade.validate()
        .then(resp => {
          if (resp) {
            this.sendForm()
          }
        })
    },

    sendForm () {
      this.$store.dispatch('carteiras/saveTrade', this.trade)
        .then(resp => {
          this.onReset()
          sucessMessage('Operação registrada com sucesso!')
        })
        .catch(error => errorMessage('Falha ao realizar operação!', error))
    },

    filterCodigo (val, update) {
      update(() => {
        const all = this.$store.state.acoes.all
        this.acoes = all.slice(0, all.length)
          .filter(v => v.codigo.indexOf(val.toUpperCase()) > -1)
      })
    },

    showFieldCompra () {
      return this.tipoTrade === 'dayTrade' || this.tipoTrade === 'compra'
    },

    showFieldVenda () {
      return this.tipoTrade === 'dayTrade' || this.tipoTrade === 'venda'
    },

    title () {
      const tipo = this.tipoTrade
      if (tipo === 'dayTrade') {
        return 'Novo day trade'
      } else if (tipo === 'compra') {
        return 'Nova compra'
      } else if (tipo === 'venda') {
        return 'Nova venda'
      }
    },

    getIcon () {
      return 'fas fa-shopping-cart'
    },

    getColor () {
      const tipo = this.tipoTrade
      if (tipo === 'dayTrade') {
        return 'orange'
      } else if (tipo === 'compra') {
        return 'green'
      } else if (tipo === 'venda') {
        return 'red'
      }
    }
  },
  directives: { money: VMoney }
}
</script>

<style scoped>
  .mBtn{
    margin: 0.3em 0 0 0;
  }
</style>
