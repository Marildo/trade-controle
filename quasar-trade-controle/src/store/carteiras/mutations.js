const SET_CARTEIRAS = (state, payload) => {
  state.all = payload
}

const SET_CARTEIRA = (state, payload) => {
  state.current = payload
}

export {
  SET_CARTEIRAS,
  SET_CARTEIRA
}
