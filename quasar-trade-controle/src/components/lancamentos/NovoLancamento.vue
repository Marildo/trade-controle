<template>
  <div >
    <q-btn flat color = "brown-6"
       icon="fas fa-retweet"
       @click="onShowForm"
    >
      <q-tooltip >
        Novo Lancamento
      </q-tooltip>
    </q-btn>

    <q-dialog v-model="showForm" persistent>
      <q-card style="width: 500px">
        <q-card-section>
          <q-avatar icon="fas fa-retweet" color = "brown-6" text-color="white" />
          <span class="q-ml-sm text-subtitle1 text-blue-grey-9">Novo Lançamento</span>
          <hr>
        </q-card-section>

        <q-form class="q-gutter-md"  ref="form" >
          <q-card-actions class="row q-pa-md flex justify-start" >
              <q-input class="q-ma-sm col-md-4 col-10"
                filled
                v-model="lancamento.carteira.nome"
                label="Carteira"
                :readonly=true
                :rules="['']"
              />

              <q-select class="q-ma-sm col-md-6 col-10"
                filled
                label ="Tipo do Lançamento *"
                v-model="lancamento.tipo"
                use-input
                hide-selected
                fill-input
                input-debounce="0"
                option-label="descricao"
                :options="tipos"
                @filter="filterTipo"
                lazy-rules
                :rules="tipoRule"
               >
               <template v-slot:no-option>
                 <q-item>
                  <q-item-section class="text-grey">
                    Tipo não localizado
                  </q-item-section>
                 </q-item>
               </template>
              </q-select>

             <q-field class="q-ma-sm col-md-4 col-10"
              filled
              v-model="lancamento.valor"
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
             </q-field>

            <q-input class="q-ma-sm col-md-6 col-10"
              filled
              v-model="lancamento.descricao"
              label="Descrição *"
              lazy-rules
              :rules="descricaoRule"
             />

             <q-input class="q-ma-sm col-10"
               filled
               v-model="lancamento.dataMovimentacao"
               label="Data"
               mask="##/##/#### ##:##:##"
              lazy-rules
              :rules="['']"
             >
               <template v-slot:prepend>
                 <q-icon name="event" class="cursor-pointer">
                   <q-popup-proxy transition-show="scale" transition-hide="scale">
                     <q-date v-model="lancamento.dataMovimentacao" mask="DD/MM/YYYY HH:mm:ss" />
                   </q-popup-proxy>
                 </q-icon>
               </template>
               <template v-slot:append>
                 <q-icon name="access_time" class="cursor-pointer">
                   <q-popup-proxy transition-show="scale" transition-hide="scale">
                     <q-time v-model="lancamento.dataMovimentacao" mask="DD/MM/YYYY HH:mm:ss" format24h />
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
  name: 'NovoLancamento',

  props: ['carteira'],

  data () {
    return {
      showForm: false,
      lancamento: {},
      tipos: [],

      moneyFormatForDirective: {
        decimal: ',',
        thousands: '.',
        precision: 2,
        masked: false
      },

      valorRule: [v => (!!v && v !== '0,00') || 'Informe o valor da operação'],
      tipoRule: [val => (val && val.key) || 'Selecione um tipo'],
      descricaoRule: [v => (!!v && v !== '')]
    }
  },

  created () {
    this.$store.dispatch('commons/loadTiposLancamentos')
    this.onReset()
  },

  methods: {
    onShowForm () {
      this.onReset()
      this.showForm = true
    },

    onReset () {
      this.showForm = false
      this.lancamento = {
        valor: 0,
        carteira: this.carteira,
        dataMovimentacao: new Date().toLocaleString()
      }
    },

    onSubmit () {
      this.$refs.form.validate()
        .then(resp => {
          if (resp) {
            this.$store.dispatch('carteiras/addLancamento', this.lancamento)
              .then(resp => {
                this.onReset()
                sucessMessage('Lançamento registrado com sucesso!')
              })
              .catch(error => errorMessage('Falha ao realizar lancamento!', error))
          }
        })
    },

    filterTipo (val, update) {
      update(() => {
        const all = this.$store.state.commons.tiposLancamentos
        this.tipos = all.slice(0, all.length)
          .filter(v => v.key > 1)
          .filter(v => v.descricao.indexOf(val.toUpperCase()) > -1)
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
