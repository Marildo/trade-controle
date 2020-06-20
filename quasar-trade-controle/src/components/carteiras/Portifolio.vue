<template>
  <div class="q-pa-md">
    <q-table
      class="table-header-grey"
      :data="portifolio"
      :columns="columns"
      :pagination.sync="pagination"
      row-key="id"
      flat
      bordered
    />
  </div>
</template>

<script>
import { formaterReal, formaterPercent } from '../../utils/numberUtils'

export default {
  name: 'Portifolio',

  data () {
    return {
      pagination: {
        rowsPerPage: 30
      },
      columns: [
        {
          name: 'codigo',
          label: 'Código',
          field: 'codigoAcao',
          align: 'left',
          sortable: true
        },
        {
          name: 'cotacao',
          label: 'Cotação',
          field: 'cotacao',
          align: 'left',
          sortable: true,
          format: val => formaterReal(val)
        },
        {
          name: 'quantidade',
          label: 'Quantidade',
          field: 'quantidade',
          align: 'left',
          style: 'width: 7vh',
          sortable: true
        },
        {
          name: 'custoTotal',
          label: 'Custo Total',
          field: 'custoTotal',
          align: 'left',
          sortable: true,
          format: val => formaterReal(val)
        },
        {
          name: 'precoMedio',
          label: 'Preço Médio',
          field: 'precoMedio',
          align: 'left',
          sortable: true,
          format: val => formaterReal(val)
        },
        {
          name: 'totalAtual',
          label: 'Total',
          field: 'totalAtual',
          align: 'left',
          sortable: true,
          format: val => formaterReal(val)
        },
        {
          name: 'resultado',
          label: 'Resultado',
          field: 'resultado',
          align: 'left',
          sortable: true,
          format: val => formaterReal(val)
        },
        {
          name: 'percentual',
          label: '%',
          field: 'percentual',
          align: 'left',
          sortable: true,
          format: val => formaterPercent(val)
        }
      ]
    }
  },

  computed: {
    portifolio () {
      return this.$store.state.carteiras.current.portifolio
    }
  }
}
</script>

<style>

</style>
