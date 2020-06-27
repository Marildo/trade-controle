<template>
  <div>
    <div class="row flex flex-center">
      <tCard title="Saldo em caixa" :content="header.saldoCaixa" />
      <tCard title="Total ações" :content="header.saldoAtivos" />
      <tCard title="Total" :content="header.saldoCaixa + header.saldoAtivos" />
      <tCard title="Resultado mensal" :content="header.resultadoMensal" />
      <tCard title="Resultado semanal" :content="header.resultadoSemanal" />
      <tCard title="Último resultado" :content="header.resultadoDiario" />
    </div>
  </div>
</template>

<script>
import tCard from '../TCard.vue'

export default {
  name: 'HeaderCarteira',
  components: { tCard },
  props: ['header']
}
</script>
