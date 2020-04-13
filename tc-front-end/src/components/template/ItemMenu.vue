<template>
  <router-link class="itemMenu" tag="li" :to="link" active-class="active" exact>{{title}}</router-link>
</template>

<script>
export default {
  name: "ItemMenu",
  props: ["title", "link"]
};
</script>

<style >
.itemMenu {
  margin: 0.3rem 0.5rem 0 0.5rem;
  height: 2rem;
  padding: 2% 0% 2% 5%;
  border-radius: 0.3rem;

  color: #f4f4f9;
  font-weight: 500;
  text-decoration: none;

  display: flex;
  justify-content: flex-start;
  align-items: center;

  cursor: pointer;
}

.itemMenu:hover {
  background-color: rgba(0, 0, 0, 0.2);
}

.active {
  background-color: rgba(28, 106, 166, 0.3);
  border: 1px solid rgba(0, 0, 0, 0.2);
  font-weight: 700;
}
</style>