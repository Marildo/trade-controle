<template>
  <div>
    <div class="row flex-center">
      <tCard title="Saldo em caixa" :content="header.saldoAcoes" />
      <tCard title="Total ações" :content="header.saldoAcoes" />
      <tCard title="Total" :content="header.saldoAcoes + header.saldoAcoes" />
      <tCard title="Último mensal" content=1000 />
      <tCard title="Último semanal" content=1000 />
      <tCard title="Último resultado" content=1000 />
      <tCard title="Último resultado" content=1000 />
      <tCard title="Último resultado" content=1000 />
      <tCard title="Último resultado" content=rrr />
    </div>
    <hr>
  </div>
</template>

<script>
import tCard from './TCard.vue'

export default {
  name: 'HeaderCarteira',
  components: { tCard },
  props: ['header'],
  mounted () {
    console.log(this.header)
  }
}
</script>
