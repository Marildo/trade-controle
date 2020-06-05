<template>
 <q-layout  id="q-app" view="hHh lpR lFf">
    <tcHeader @changeDrawer="drawer = !drawer" />

    <q-drawer show-if-above v-model="drawer" side="left" bordered >
     <tcMenu/>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <tcFooter />
  </q-layout>
</template>

<script>

import tcMenu from './layouts/Menu'
import tcHeader from './layouts/Header'
import tcFooter from './layouts/Footer'

export default {
  name: 'App',

  components: {
    tcMenu,
    tcHeader,
    tcFooter
  },

  data () {
    return {
      drawer: false
    }
  }
}
</script>
