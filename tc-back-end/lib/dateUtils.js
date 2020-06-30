const startOfMonth = (date) => {
  if (date instanceof Date) {
    const month = date.getMonth()
    const year = date.getFullYear()
    return new Date(year, month, 01)
  }
  return undefined
}

module.exports = {
  startOfMonth,
}
