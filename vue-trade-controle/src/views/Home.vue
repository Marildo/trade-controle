<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <v-btn   @click="onClick">Alterar Patrimonio</v-btn>
  </div>
</template>

<script>

export default {
  name: 'Home',
  components: {

  },

  methods: {
    onClick(){
      console.log("Clicando");
      this.$store.state.dashboard.totalGeral =999      
    }
  },
}
</script>
