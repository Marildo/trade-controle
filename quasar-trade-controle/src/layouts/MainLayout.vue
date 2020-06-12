<template>
  <q-layout view="hHh lpR lFf">
    <tcHeader @changeDrawer="drawer = !drawer" />

    <q-drawer show-if-above v-model="drawer" side="left" bordered width="100">
     <tcMenu/>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <tcFooter />
  </q-layout>
</template>

<script>
import tcMenu from './Menu'
import tcHeader from './Header'
import tcFooter from './Footer'

export default {
  components: {
    tcMenu,
    tcHeader,
    tcFooter
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
