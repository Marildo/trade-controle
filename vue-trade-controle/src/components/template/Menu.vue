<template>
  <v-navigation-drawer v-model="showMenu" app clipped>
    <v-list dense>
      <ItemMenu title="Dashboard" routeName="Home" icon="mdi-view-dashboard" />
      <ItemMenu title="Carteiras" routeName="CarteirasIndex" icon="mdi-wallet" />
      <ItemMenu title="Açoes" routeName="Acoes" icon="mdi-file-multiple" />
      <ItemMenu title="Setores" routeName="Setores" icon="mdi-chart-arc" />
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
    ...mapState({
      isMenuVisible: state => state.isMenuVisible
    }),

    showMenu: {
      get() {
        return this.isMenuVisible;
      },
      set(v) {
        v // nao faz nada, só para remover o erro do console
      }
    }
  }
};
</script>

<style>
</style>