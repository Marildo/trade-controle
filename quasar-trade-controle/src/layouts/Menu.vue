<template>
      <q-list>
        <q-item-label header class="text-grey-8">Menu</q-item-label>
        <section v-for="item in items" :key="item.title" class="text-indigo-8">
            <q-item clickable :to="item.route">
                <q-item-section  v-if="item.icon" avatar>
                  <q-icon :name="item.icon" />
                </q-item-section>

                <q-item-section>
                 <q-item-label>{{ item.title }}</q-item-label>
                </q-item-section>
            </q-item>
        </section>
     </q-list>
</template>

<script>
export default {
  name: 'Menu',

  data () {
    return {
      items: [
        { title: 'Dashboard', icon: 'dashboard', route: { name: 'Dashboard' } },
        { title: 'Carteiras', icon: 'account_balance_wallet', route: { name: 'Carteiras' } },
        { title: 'Ações', icon: 'insights', route: { name: 'Acoes' } }
      ]
    }
  }
}
</script>

<style>

</style>
