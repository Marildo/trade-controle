const localDateToYYYMMdd = (date) => {
    const local = date.toLocaleDateString().split('/')
    return local[2] +'-'+local[1]+'-'+local[0]
}

module.exports = {
    localDateToYYYMMdd
}