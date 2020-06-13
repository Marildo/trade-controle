<template>
  <div class="q-pa-md">
    <q-table
      class="table-header-grey"
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
        },
        {
          label: 'Excluir'
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
