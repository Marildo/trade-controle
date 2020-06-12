const SET_CARTEIRAS = (state, payload) => {
  state.all = payload
}

const SET_CARTEIRA = (state, payload) => {
  state.current = payload
}

const SET_SUM = (state, payload) => {
  state.sum = payload
}

const SET_LANCAMENTOS = (state, payload) => {
  state.lancamentos = payload
}

export {
  SET_CARTEIRAS,
  SET_CARTEIRA,
  SET_SUM,
  SET_LANCAMENTOS
}
