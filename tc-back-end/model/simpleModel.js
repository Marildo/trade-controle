const db = require('../config/db')

const selectSimple = async (table, id) => {
    const result = await db(table)
        .where('id', id)
        .first()
        .catch((error) => console.log(error))
    return result
}

const insertSimple = async (table, simple) => {
    const result = await db(table)
        .insert(simple)
        .returning('*')
        .catch((error) => console.log(error))
    return result[0]
}

// Setores
const selectSetor = async (id) => {
    return await selectSimple('setores', id)
}

const saveSetor = async (setor) => {
    const isExist = await selectSetor(setor.id)
    if (isExist)
        return isExist

    return await insertSimple('setores', setor)
}



// Subsetores
const selectSubsetor = async (id) => {
    return await selectSimple('subsetores', id)
}

const saveSubsetor = async (subsetor) => {
    const isExist = await selectSubsetor(subsetor.id)
    if (isExist)
        return isExist

    return await insertSimple('subsetores', subsetor)
}

// segmentos
const saveSegmento = async (segmento) => {
    const isExist = await selectSegmento(segmento.id)
    if (isExist)
        return isExist

    return await insertSimple('segmentos', segmento)
}

const selectSegmento = async (id) => {
    return await selectSimple('segmentos', id)
}

module.exports = {
    selectSetor,
    saveSetor,

    selectSubsetor,
    saveSubsetor,

    saveSegmento,
    selectSegmento
}
