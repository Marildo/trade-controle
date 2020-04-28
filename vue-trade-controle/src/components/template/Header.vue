<template>
  <v-app-bar app clipped-left >
    <v-app-bar-nav-icon @click="toggleMenu" />
    <v-toolbar-title>Trade Controle</v-toolbar-title>
     <Toast />
  </v-app-bar>
</template>

<script>
import Toast from 'primevue/toast';

export default {
  name: "Header",

  components: {
    Toast
  },

  methods: {
    toggleMenu() {
      this.$store.commit("toggleMenu")
    }
  }
}
</script>

<style>
</style>