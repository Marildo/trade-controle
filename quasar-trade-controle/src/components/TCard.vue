<template>
  <div class="box col-md-3 col-12">
    <div class="text-subtitle1 text-blue-grey-9"> {{ title }} </div>
    <div class="text-body2 text-blue-grey-6"> {{ content | formaterReal }} </div>
  </div>
</template>

<script>
// import * as numberUtils from '../utils/numberUtils'

export default {
  name: 'TCard',
  props: ['title', 'content']
  /* filters: {
    formaterReal (value) {
      return numberUtils.formaterReal(value)
    }
  }
  */
}
</script>

<style scoped>
  .box {
    margin: .3em;
    padding: .3em;
    box-shadow: 1px 1px 1px 1px rgb(202, 203, 206);
    text-align: center;
  }
</style>
