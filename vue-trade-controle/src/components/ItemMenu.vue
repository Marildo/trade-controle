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
  props: ["title", "link","icon"],

  methods: {
    navegateTo() {
      this.$router.push(this.link);
    }
  }
}
</script>

<style >
</style>