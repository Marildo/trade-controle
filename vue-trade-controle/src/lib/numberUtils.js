function formaterReal(value) {
    if (isNaN(value))
        value = 0

    return value.toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL',
    })
}

function formaterPercent(value) {
    if (isNaN(value))
        value = 0
    return value.toLocaleString('pt-BR', { style: 'decimal' }) + ' %'
}

export {
    formaterReal,
    formaterPercent
}