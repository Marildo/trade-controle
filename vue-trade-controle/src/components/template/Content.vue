<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout >
        <v-flex shrink>
          <v-col class="col-12">
            <router-view/>
          </v-col>          
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