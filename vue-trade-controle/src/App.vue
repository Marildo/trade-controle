<template>
  <div id="app">
    <v-app id="inspire">
      <Menu />
      <Header />
      <Content />
      <Footer />
    </v-app>
  </div>
</template>

<script>
import Header from "@/components/template/Header.vue";
import Menu from "@/components/template/Menu.vue";
import Content from "@/components/template/Content.vue";
import Footer from "@/components/template/Footer.vue";

import {loadAcoes} from "@/controllers/acaoController"
import {loadCarteiras} from "@/controllers/carteiraController"

export default {
  name: "App",

  components: {
    Header,
    Menu,
    Content,
    Footer
  },

  data: () => ({

  }),

  created() {
    this.$vuetify.theme.dark = true;
  },

  mounted() {
     loadAcoes()
     loadCarteiras()
  },

  methods: {

  }
};
</script>
