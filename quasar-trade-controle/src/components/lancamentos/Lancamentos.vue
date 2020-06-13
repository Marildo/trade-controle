<template>
  <div class="q-pa-md">
    <q-table
      class="my-sticky-header-table"
      :data="lancamentos"
      :columns="columns"
      row-key="id"
      flat
      bordered >
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
          >
            {{ col.value }}
          </q-td>
          <q-td auto-width>
            <q-btn size="sm"
              color="red"
              icon="delete"
              round dense
              @click="deleteLancamento(props)"  />
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
</template>

<script>
import { formaterReal } from '../../utils/numberUtils'

export default {
  name: 'Lancamentos',

  data () {
    return {
      columns: [
        {
          name: 'data',
          required: true,
          label: 'Data',
          align: 'left',
          field: 'dataMovimentacao',
          format: val => new Date(parseInt(val)).toLocaleDateString(),
          sortable: true
        },
        {
          name: 'valor',
          align: 'left',
          label: 'Valor',
          field: 'valor',
          format: val => formaterReal(val),
          sortable: true
        },
        {
          name: 'descricao',
          align: 'left',
          label: 'Descricao',
          field: 'descricao'
        },
        {
          name: 'tipo',
          align: 'left',
          label: 'Tipo',
          field: row => row.tipoLancamento.descricao,
          sortable: true
        }
      ]
    }
  },

  computed: {
    lancamentos () {
      return this.$store.state.carteiras.lancamentos
    }
  },

  methods: {
    deleteLancamento ({ row }) {
      this.$store.dispatch('carteiras/deleteLancamento', row)
    }
  }
}
</script>

<style lang="sass">
.my-sticky-header-table
  .q-table__top,
  .q-table__bottom,
  thead tr:first-child th
    /* bg color is important for th; just specify one */
    background-color: $blue-grey-2

  thead tr th
    position: sticky
    z-index: 1
  thead tr:first-child th
    top: 0

  /* this is when the loading indicator appears */
  &.q-table--loading thead tr:last-child th
    /* height of all previous header rows */
    top: 48px
</style>
