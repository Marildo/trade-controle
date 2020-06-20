<template>
  <div>
    <q-btn
      color="primary"
      icon="add_circle"
      flat
      rounded
      @click="setShowForm()"
    >
      <q-tooltip> Nova Carteira </q-tooltip>
    </q-btn>
    <q-dialog v-model="showForm" persistent>
      <q-card  style="width: 300px">
        <q-card-section>
          <q-avatar icon="add_circle" color="primary" text-color="white" />
          <span class="q-ml-sm text-subtitle1 text-blue-grey-9"
            >Nova carteira</span
          >
          <hr />
        </q-card-section>

        <q-form class="q-gutter-md" ref="form">
          <q-card-actions class="row q-pa-md flex justify-start">
            <q-input
              class="q-ma-sm col-12"
              filled
              v-model="nome"
              label="Carteira"
              :rules="nomeRule"
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
import { errorMessage } from '../../utils/message'

export default {
  data () {
    return {
      showForm: false,
      nome: '',
      nomeRule: [
        (val) =>
          (val && val.length > 3) ||
          'Nome da carteira deve ter no mínimo 4 caracteres'
      ]
    }
  },

  methods: {
    setShowForm () {
      this.nome = ''
      this.showForm = true
    },

    onSubmit () {
      this.$store.dispatch('carteiras/addCarteira', this.nome)
        .then(this.showForm = false)
        .catch(error => errorMessage('Falha ao realizar operação!', error))
    }
  }
}
</script>

<style></style>
