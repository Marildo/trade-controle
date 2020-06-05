<template>
  <q-layout view="hHh lpR lFf">
    <Header @changeDrawer="drawer = !drawer" />

    <q-drawer show-if-above v-model="drawer" side="left" bordered>
     <Menu/>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer elevated class="bg-grey-8 text-white">
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo/svg/quasar-logo.svg">
          </q-avatar>
          Title
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>

  </q-layout>
</template>

<script>
import Menu from './Menu.vue'
import Header from './Header'
export default {
  components: {
    Menu,
    Header
  },

  data () {
    return {
      drawer: false
    }
  },

  methods: {

  }
}
</script>
