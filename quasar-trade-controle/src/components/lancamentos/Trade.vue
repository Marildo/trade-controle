<template>
  <div >
    <q-btn flat :color = "isBuy ? 'green' : 'red'"
       icon="fas fa-shopping-cart"
       @click="showForm = true"
    >
      <q-tooltip >
         {{isBuy ? "Nova Compra" : "Nova Venda" }}
      </q-tooltip>
    </q-btn>

    <q-dialog v-model="showForm" persistent>
      <q-card>
        <q-card-section>
          <q-avatar icon="fas fa-shopping-cart" :color = "isBuy ? 'green' : 'red'" text-color="white" />
          <span class="q-ml-sm text-subtitle1 text-blue-grey-9">{{ isBuy ? "Compra" : "Venda"}} de ações</span>
          <hr>
        </q-card-section>

        <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md" >
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

             <q-field class="q-ma-sm col-md-3 col-5"
              filled
              v-model="trade.valor"
              label="Valor *"
              prefix= 'R$ '
              lazy-rules
              :rules="valorRule"
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

             <q-checkbox class="q-ma-sm col-md-4 col-10"
              v-model="trade.continue"
              label="Salvar e continuar"
             />
            </q-card-actions>
            <q-card-actions align="right" class="row bg-blue-grey-14 shadow-box shadow-3">
              <q-btn label="Cancelar" type="reset" color="negative" class="mBtn col-md-2 col-12" />
              <q-btn label="Salvar"  type="submit" color="positive" class="mBtn col-md-2 col-12" />
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

  props: ['carteira', 'isBuy'],

  data () {
    return {
      showForm: false,
      acoes: [],
      trade: {},

      moneyFormatForDirective: {
        decimal: ',',
        thousands: '.',
        precision: 2,
        masked: false /* doesn't work with directive */
      },

      quantidadeRule: [v => (!!v && parseInt(v) > 0) || 'Informe a quantidade'],
      valorRule: [v => (!!v && parseFloat(v.replace(',', '.')) >= 0.05) || 'Valor deve ser maior 0,05'],
      acaoRule: [val => (val && val.codigo.length > 3) || 'Selecione uma ação']
    }
  },

  created () {
    this.acoes = this.$store.state.acoes.all
    this.onReset()
  },

  methods: {
    onReset () {
      this.showForm = false
      this.trade = {
        valor: '10,00',
        carteira: this.carteira,
        acao: { codigo: '', preco: '0,00' },
        quantidade: '100',
        continue: false,
        compra: this.isBuy,
        dataTrade: new Date().toLocaleString()
      }
    },

    onSubmit () {
      this.$store.dispatch('carteiras/saveTrade', this.trade)
        .then(resp => {
          sucessMessage('Operação registrada com sucesso!')
          this.onReset()
        })
        .catch(error => errorMessage('Falha ao realizar operação!', error))
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
  .mBtn{
    margin: 0.3em 0 0 0;
  }
</style>
