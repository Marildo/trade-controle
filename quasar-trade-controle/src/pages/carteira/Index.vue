<template>
  <div>
     <div class="row">
       <div class="col-md-4 col-12" v-for="carteira in carteiras" :key="carteira.id">
          <div class="carteira">
              <div class="text-blue-8 text-h4  ">{{carteira.nome}}</div>
              <div class="text-teal-5 text-h6  ">Caixa: {{carteira.saldoCaixa}}</div>
              <div class="text-teal-5 text-h6  ">Ações: {{carteira.saldoAcoes}}</div>
              <div class="text-teal-5 text-h6  ">Total: {{carteira.saldoCaixa + carteira.saldoAcoes}}</div>
              <div> <hr></div>
              <div class="actions">
                <q-btn flat color="primary" icon="fas fa-eye"
                 :to="{
                   name: 'Carteira',
                   params: { id: carteira.id }
                  }"
                />
                <q-btn flat color="green" icon="fas fa-shopping-cart" />
                <q-btn flat color="red" icon="fas fa-shopping-cart" />
                <q-btn flat color="orange" icon="fas fa-retweet" />
              </div>
          </div>
       </div>
     </div>
  </div>
</template>

<script>
export default {
  name: 'Cateiras',

  mounted () {
    this.$store.dispatch('carteiras/loadCarteiras')
  },

  computed: {
    carteiras () {
      return this.$store.state.carteiras.all
    }
  }
}
</script>

<style scoped>
  .carteira {
    display: flex;
    flex-direction: column;
    padding: 1em;
    margin: .5em;
    background: #eeffee;
    box-shadow: 1px 1px 1px 0px rgba(181,199,230,1);
  }
  .actions {
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
  }
</style>
