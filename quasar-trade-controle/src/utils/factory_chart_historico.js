
const buildChartHistorico = (historico) => {
  const getData = (item) => {
    item.data = new Date(
      parseInt(item.dataHistorico)
    ).toLocaleDateString('pt-BR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    })
    delete item.dataHistorico
    return item
  }

  const somaSaldo = (item) => {
    item.saldo = item.saldoAtivos + item.saldoCaixa
    delete item.saldoAtivos
    delete item.saldoCaixa
    return item
  }

  const keys = Array.from(new Set(historico.map((i) => i.title)))
  keys.unshift('data')
  keys.push('Total')

  const fase1 = historico.map(getData)
  const fase2 = fase1.map(somaSaldo)
  const datas = Array.from(new Set(fase2.map((i) => i.data)))

  const fase4 = []
  for (let i = 0; i < datas.length; i++) {
    const values = fase2.filter((item) => item.data === datas[i])
    fase4.push(values)
  }

  const totaliza = (item) => {
    const agg = {}
    for (let index = 0; index < item.length; index++) {
      const element = item[index]
      agg.data = element.data
      agg[element.title] = element.saldo
    }

    const total = item.map((i) => i.saldo).reduce((c, n) => c + n)
    agg.Total = total
    return agg
  }

  const fase5 = fase4.map(totaliza)

  return {
    columns: keys,
    rows: fase5
  }
}

const groupTotalByData = (historicos) => {
  const result = []
  const datas = Array.from(new Set(historicos.map((i) => i.data)))
  for (const dia of datas) {
    const total = historicos.filter(v => v.data === dia).map(v => v.saldo).reduce((c, n) => c + n)
    const row = {
      data: dia,
      total
    }
    result.push(row)
  }
  return result
}

export { buildChartHistorico, groupTotalByData }
