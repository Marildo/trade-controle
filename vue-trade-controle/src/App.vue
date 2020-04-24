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


export default {
  name: "App",

  components: {
    Header,
    Menu,
    Content,
    Footer,
  },

  data: () => ({
    drawer: null
  }),

  created() {
   this.$vuetify.theme.dark = true;
  }
};
</script>
