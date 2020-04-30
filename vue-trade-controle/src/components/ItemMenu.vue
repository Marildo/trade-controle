<template>
  <v-list-item @click="navegateTo">
    <v-list-item-action>
      <v-icon>{{icon}}</v-icon>
    </v-list-item-action>
    <v-list-item-content>
      <v-list-item-title>{{title}}</v-list-item-title>
    </v-list-item-content>
  </v-list-item>
</template>

<script>
export default {
  name: "ItemMenu",

  props: ["title", "routeName", "icon"],

  methods: {
    navegateTo() {
      const correntRoute = this.$router.currentRoute.name
      if (correntRoute != this.routeName){
        this.$router
          .push({name: this.routeName} )
          .catch(erro => {
            console.log( erro);
          })
      }else{
         this.$router.go(0)
      }
    }
  }
};
</script>

<style >
</style>