<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout >
        <v-flex shrink>
          <router-view/>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
export default {
  name: "Content"
};
</script>

<style>
</style>