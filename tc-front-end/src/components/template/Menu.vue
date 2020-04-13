<template>
  <nav class="menu" v-show="isMenuVisible">
    <ul>
      <ItemMenu title="Dashboard" link="/" />
      <ItemMenu title="Carteiras" link="carteiras" />
      <ItemMenu title="Ações" link="acoes" />
      <ItemMenu title="Setores" link="setores" />
    </ul>
  </nav>
</template>

<script>
import { mapState } from "vuex";
import ItemMenu from "@/components/template/ItemMenu";

export default {
  components: { ItemMenu },
  name: "Menu",
  computed: mapState(["isMenuVisible"])
};
</script>

<style>
.menu {
  grid-area: menu;
  background: linear-gradient(to right, #1c6aa6, #76acd6);

  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
}

.menu >ul{
  padding: 0;
  margin: 0;
}
</style>