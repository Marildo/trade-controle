<template>
  <div>
    <h1>Acoes</h1>
    <button @click="loadAcoes">Obter acoes</button>
    <hr>
    <ul>
      <li v-for='acao in acoes' :key='acao.codigo'> {{acao.codigo}} - {{acao.empresa}}</li>
    </ul>
  </div>
</template>

<script>
import gql from "graphql-tag";

export default {
  name: "Acoes",

  data() {
    return {
      acoes: []
    };
  },

  methods: {
    loadAcoes() {
      this.$api
        .query({
          query: gql`
            {
              acoes {
                codigo
                empresa
              }
            }
          `
        })
        .then(resp => (this.acoes = resp.data.acoes))
        .catch(err => console.log(err));
    }
  }
}
</script>

<style>
</style>