import vue from 'vue'

function showToast(severity, summary, detail, life) {
    vue.prototype.$toast.add({
        severity,
        summary,
        detail,
        life
    });
}

function showToastSuccess(detail, summary, life) {
    vue.prototype.$toast.add({
        severity: "success",
        summary: summary || 'Operação realizada com sucesso!',
        detail: detail || '',
        life: life || 3000
    });
}


function showToastError(detail, summary, life) {
    vue.prototype.$toast.add({
        severity: "error",
        summary: summary || 'Falha ao realizar operação!',
        detail: detail || '',
        life: life || 20000
    });
}

// TODO destrinchar a menssagem function externa
function catchError(error) {
    let tryError = error
    if (error.networkError) {
        tryError = error.networkError
        if (tryError.result) {
            tryError = tryError.result
            if (tryError.errors) {
                tryError = tryError.errors[0].message
            }
        }
    }
    console.log("try:", tryError)
    showToastError(tryError || undefined); // replace em Error: "GraphQL error:
}

export {
    showToast,
    showToastSuccess,
    showToastError,
    catchError
}
