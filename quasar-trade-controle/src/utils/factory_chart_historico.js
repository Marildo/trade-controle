const build = (historico) => {
  // console.log(historico)

  const keys = Array.from(new Set(historico.map((i) => i.title)))
  keys.unshift('data')

  const fase1 = historico.map(getData)
  const fase2 = fase1.map(criarTitulos)
  const fase3 = fase2.map(somaSaldo)

  // console.log(fase3)

  const datas = Array.from(new Set(fase3.map((i) => i.data)))

  const fase4 = []
  for (let i = 0; i < datas.length; i++) {
    const values = fase3.filter((item) => item.data === datas[i])
    fase4.push(values)
  }

  const fase5 = []
  for (const value of fase4) {
    const obj = {}
    for (const v of value) {
      for (const key of keys) {
        if (v[key]) obj[key] = v[key]
      }
    }
    fase5.push(obj)
  }
  return {
    columns: keys,
    rows: fase5
  }
}

const getData = (item) => {
  const key = 'data'
  item[key] = new Date(parseInt(item.dataHistorico)).toLocaleDateString(
    'pt-BR',
    {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    }
  )
  delete item.dataHistorico
  return item
}

const criarTitulos = (item) => {
  item[item.title] = 0
  return item
}

const somaSaldo = (item) => {
  item[item.title] = item.saldoAtivos + item.saldoCaixa
  delete item.saldoAtivos
  delete item.saldoCaixa
  delete item.title
  return item
}

export { build }
