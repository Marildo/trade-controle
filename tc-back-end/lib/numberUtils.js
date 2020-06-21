function formateReal(value) {
  if (isNaN(value)) value = 0

  const str = value.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  })

  return str
    .replace('.', '&')
    .replace(',', '.')
    .replace(',', '.')
    .replace('&', ',')
}

module.exports = {
  formateReal
}
