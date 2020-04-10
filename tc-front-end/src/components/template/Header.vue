<template>
    <header class="header">Header</header>
</template>

<script>
export default {
    name:"Header"
}
</script>

<style scoped>
    .header {
        grid-area: header;
        background: linear-gradient(to top, #1c6aa6, #76acd6);

        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>