<template>
  <v-app-bar app clipped-left>
    <v-app-bar-nav-icon @click="toggleMenu" />
    <v-toolbar-title>Trade Controle</v-toolbar-title>
    <v-spacer></v-spacer>

    <span class="saldo">
      <v-icon large color="amber lighten-2">fa-university</v-icon>
      Patrimônio Total: {{patrimonio.total | formaterReal}}
    </span>

    <Toast />
  </v-app-bar>
</template>

<script>
import Toast from "primevue/toast";

export default {
  name: "Header",

  components: {
    Toast
  },

  computed: {
    patrimonio(){
        return this.$store.getters.patrimonio
    }
  },

  methods: {
    toggleMenu() {
      this.$store.commit("toggleMenu");
    }
  }
};
</script>

<style>
</style>