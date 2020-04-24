<template>
  <v-app-bar app clipped-left>
    <v-app-bar-nav-icon @click="toggleMenu" />
    <v-toolbar-title>Trade Controle</v-toolbar-title>
  </v-app-bar>
</template>

<script>
export default {
  name: "Header",

  methods: {
    toggleMenu() {
      this.$store.commit("toggleMenu")
    }
  }
};
</script>

<style>
</style>