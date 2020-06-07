const loadAcoes = ({ commit }) => {
  console.log('loading acoes')
  commit('SET_ACOES', [1, 5, 6])
}

export {
  loadAcoes
}
