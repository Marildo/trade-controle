<template>
   <div id="app">
     <Header />
     <Menu />
     <Content />
     <Footer />
   </div>
</template>

<script>

import Header from '@/components/template/Header'
import Menu from '@/components/template/Menu'
import Content from '@/components/template/Content'
import Footer from '@/components/template/Footer'

export default {
  name:"App",
  components: {Header, Menu, Content, Footer}
}
</script>

<style  >
   *{
     font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
   }

   body {
     background: #e4e4e4;
     margin: 0;     
   }

  #app {
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;

		height: 100vh;
		display: grid;
		grid-template-rows: 8vh 1fr 5vh;
		grid-template-columns: 30vh 1fr;
		grid-template-areas:
			"header header"
			"menu content"
			"menu footer";
  }
</style>
