<template>
  <div>
    <div class="row flex flex-center">
      <tCard title="Saldo em caixa" :content="header.saldoCaixa" />
      <tCard title="Total ações" :content="header.saldoAcoes" />
      <tCard title="Total" :content="header.saldoCaixa + header.saldoAcoes" />
      <tCard title="Último mensal" :content="header.resultadoMensal" />
      <tCard title="Último semanal" :content="header.resultadoSemanal" />
      <tCard title="Último resultado" :content="header.ultimoResultado" />
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
