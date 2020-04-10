<template>
    <aside class="menu">Menu</aside>
</template>

<script>
export default {
    name:'Menu'
}
</script>

<style>
    .menu {
        grid-area: menu;
        background: linear-gradient(to right, #1c6aa6, #76acd6);

        display: flex;
        flex-direction: column;
        flex-wrap: wrap;
    }
</style>