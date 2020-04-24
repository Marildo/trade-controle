<template>
  <v-navigation-drawer v-model="isMenuVisible" app clipped>
    <v-list dense>
      <ItemMenu title="Dashboard" link="/" icon="mdi-view-dashboard" />
      <ItemMenu title="Carteiras" link="carteiras" icon="mdi-wallet" />
      <ItemMenu title="Açoes" link="acoes" icon="mdi-file-multiple" />
      <ItemMenu title="Setores" link="setores" icon="mdi-chart-arc" />
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import ItemMenu from "@/components/ItemMenu.vue";
import { mapState } from "vuex";

export default {
  name: "Menu",

  components: {
    ItemMenu
  },

  computed: {
    ...mapState(["isMenuVisible"])
  }
};
</script>

<style>
</style>