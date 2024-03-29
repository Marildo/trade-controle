const formaterReal = (value) => {
  if (isNaN(value)) {
    value = 0
  }
  return value.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  })
}

const formaterPercent = (value) => {
  if (isNaN(value)) {
    value = 0
  }
  return value.toLocaleString('pt-BR', { style: 'decimal' }) + ' %'
}

const stringToFloat = (value) => {
  value = value.replace(/\./g, '').replace(',', '.')
  return parseFloat(value)
}

export {
  formaterReal,
  formaterPercent,
  stringToFloat
}
