function formateReal(value) {
    if (isNaN(value))
        value = 0

    return value.toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL',
    })
}

export {
    formateReal
}