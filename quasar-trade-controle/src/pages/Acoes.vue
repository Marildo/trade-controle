<template>
  <div class="q-pa-md">
    <q-toolbar>
      <q-space />
      <tNovaAcao />
    </q-toolbar>
    <q-table
      class="table-header-grey"
      :data="acoes"
      :columns="columns"
      :pagination.sync="pagination"
      row-key="id"
      flat
      bordered />
  </div>
</template>

<script>
import { formaterReal } from '../utils/numberUtils'
import tNovaAcao from '../components/acoes/NovaAcao'

export default {
  name: 'Acoes',

  components: {
    tNovaAcao
  },

  data () {
    return {
      pagination: {
        rowsPerPage: 30
      },
      columns: [
        {
          name: 'codigo',
          label: 'Código',
          field: 'codigo',
          align: 'left',
          sortable: true
        },
        {
          name: 'empresa',
          label: 'Empresa',
          field: 'empresa',
          align: 'left',
          sortable: true
        },
        {
          name: 'preco',
          label: 'Preco',
          field: 'preco',
          align: 'left',
          sortable: true,
          format: val => formaterReal(val)
        },
        {
          name: 'setor',
          label: 'Setor',
          field: row => row.setor.nome,
          align: 'left',
          sortable: true
        },
        {
          name: 'subSetor',
          label: 'SubSetor',
          field: row => row.subsetor.nome,
          align: 'left',
          sortable: true
        },
        {
          name: 'segmento',
          label: 'Segmento',
          field: row => row.segmento.nome,
          align: 'left',
          sortable: true
        }
      ]
    }
  },

  mounted () {
    this.$store.dispatch('acoes/loadAcoes')
  },

  computed: {
    acoes () {
      return this.$store.state.acoes.all
    }
  }
}
</script>

<style>

</style>
