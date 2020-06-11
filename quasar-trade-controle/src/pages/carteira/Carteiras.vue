<template>
    <div>
      <theader-carteira :header="carteira" />
      <router-view></router-view>
    </div>
</template>

<script>
import theaderCarteira from '../../components/HeaderCarteira.vue'
export default {
  name: 'IndexCarteira',
  components: { theaderCarteira },
  computed: {
    carteira () {
      return this.$store.state.carteiras.current
    }
  }
}
</script>
