<template>
      <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="changeDrawer" />

        <q-toolbar-title>
          <q-icon name="monetization_on" flat size="2rem" />
          Trade Controler
        </q-toolbar-title>
      </q-toolbar>
    </q-header>
</template>

<script>
export default {
  name: 'Header',

  methods: {
    changeDrawer () {
      this.$emit('changeDrawer')
    }
  }

}
</script>

<style>

</style>
