const save = (table, dados) => {
    return new Promise((resolve, reject) => {
        table()
            .insert(dados)
            .returning('*')
            .then(resp => {
                resolve(resp[0])
                //  console.log(resp)
            })
            .catch(error => {
                console.log(error)
                reject(error.detail)
            })
    })
}

const findAll = (table) => {
    console.log(table)
    return new Promise((resolve, reject) => {
        table()
            .select()
            .then(resp => resolve(resp))
            .catch(error => {
                console.log(error)
                reject(error.detail)
            })
    })
}

const findById = (table, id) => {
    return new Promise((resolve, reject) => {
        table()
            .select()
            .where('id', id)
            .first()
            .then(resp => resolve(resp))
            .catch(error => {
                console.log(error)
                reject(error.detail)
            })
    })
}

const deleteById = (table, id) => {
    return new Promise((resolve, reject) => {
        table()
            .delete()
            .where('id',id)
            .then(resp => resolve(resp))
            .catch(error => {
                console.log(error)
                reject(error.detail)
            })        
        })
    }

module.exports = {
            save,
            findAll,
            findById,
            deleteById
        }