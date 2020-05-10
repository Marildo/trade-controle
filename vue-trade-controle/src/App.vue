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

import CarteiraController from "@/controllers/carteiraController";
import AcaoController from "@/controllers/acaoController"

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
    // TODO Criar um metodo unico 
    new CarteiraController().loadCarteiras()
    new AcaoController().loadAcoes()
  },

  methods: {

  }
};
</script>
