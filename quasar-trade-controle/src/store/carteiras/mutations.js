const SET_CARTEIRAS = (state, payload) => {
  state.all = payload
}

const SET_CARTEIRA = (state, payload) => {
  state.current = payload
}

const UPDATE_CARTEIRAS = (state, payload) => {
  const carteiras = state.carteiras
  const index = carteiras.findIndex(i => i.id === payload.id)
  carteiras.splice(index, 1, payload)
}

const SET_SUM = (state, payload) => {
  state.sum = payload
}

const SET_LANCAMENTOS = (state, payload) => {
  state.lancamentos = payload
}

const ADD_LANCAMENTO = (state, payload) => {
  state.lancamentos.push(payload)
}

const REMOVE_LANCAMENTO = (state, payload) => {
  const lancamentos = state.lancamentos
  const index = lancamentos.findIndex(i => i.id === payload.id)
  lancamentos.splice(index, 1)
}

export {
  SET_CARTEIRAS,
  SET_CARTEIRA,
  SET_SUM,

  SET_LANCAMENTOS,
  ADD_LANCAMENTO,
  REMOVE_LANCAMENTO,
  UPDATE_CARTEIRAS
}
