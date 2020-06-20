<template>
  <div>
    <q-btn
      color="primary"
      icon="add_circle"
      flat
      rounded
      @click="setShowForm()"
    >
      <q-tooltip> Adicionar uma Ação </q-tooltip>
    </q-btn>
    <q-dialog v-model="showForm" persistent>
      <q-card  style="width: 300px">
        <q-card-section>
          <q-avatar icon="add_circle" color="primary" text-color="white" />
          <span class="q-ml-sm text-subtitle1 text-blue-grey-9"
            >Nova Ação</span
          >
          <hr />
        </q-card-section>

        <q-form class="q-gutter-md" ref="form">
          <q-card-actions class="row q-pa-md flex justify-start">
            <q-input
              class="q-ma-sm col-12"
              filled
              v-model="codigo"
              label="Código da Ação"
              :rules="codigoRule"
            />
          </q-card-actions>
          <q-card-actions
            align="right"
            class="row bg-blue-grey-14 shadow-box shadow-3"
          >
            <q-btn
              label="Cancelar"
              @click="showForm = false"
              type="button"
              color="negative"
              class="mBtn col-md-4 col-12"
            />
            <q-btn
              label="Salvar"
              @click="onSubmit"
              type="button"
              color="positive"
              class="mBtn col-md-4 col-12"
            />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
// TODO - Criar um componente com botoes dos formularios

import { sucessMessage, errorMessage } from '../../utils/message'

export default {
  name: 'NovaAcao',

  data () {
    return {
      showForm: false,
      codigo: '',
      codigoRule: [
        (val) =>
          (val && val.length >= 5 && val.length <= 6) ||
          'Informe o código da ação com 5 ou 6 caracteres'
      ]
    }
  },

  methods: {
    setShowForm () {
      this.codigo = ''
      this.showForm = true
    },

    onSubmit () {
      this.$store.dispatch('acoes/addAcao', this.codigo)
        .then(() => {
          this.showForm = false
          sucessMessage('Ação adicionada com sucesso!')
        })
        .catch(e => {
          errorMessage('Falha ao adicionar ação!', e.message)
        })
    }
  }
}
</script>

<style></style>
