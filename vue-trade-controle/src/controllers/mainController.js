import store from '../store';

import CarteiraController from "./carteiraController";
import { ctrlLoadAcoes, ctrlSaveAcao } from "./acaoController"
import { showToastSuccess, showToastError } from "@/lib/messages"

const loadAcoes = () => {
    ctrlLoadAcoes()
        .then(resp => store.commit('setAcoes', resp.data.acoes))
        .catch(error => {
            console.log(error)
            console.log(error.networkError.result.errors)
        })
}

const loadCarteiras = () => {
    new CarteiraController()
        .loadCarteiras()
        .then(resp => setCarteiras(resp.data.carteiras))
        .catch(error => {
            console.log(error)
            console.log(error.networkError.result.errors)
        })
}

const setCarteiras = (carteiras) => {
    store.commit('carteiras', carteiras)
    setPatrimonio(carteiras)
}

const setPatrimonio = (carteiras) => {
    const calcTotalGeral = (carteiras) => carteiras.map(c => c.saldoCaixa + c.saldoAcoes).reduce((c, n) => c + n)
    let totalGeral = calcTotalGeral(carteiras)
    store.commit('patrimonio', totalGeral)
}


const init = () => {
    loadCarteiras()
    loadAcoes()
}

const setCarteira = (carteira) => {
    const dashboard = store.getters.dashboard
    const index = dashboard.carteiras.findIndex(i => i.id == carteira.id)
    const carteiras = dashboard.carteiras.splice(index, 1, carteira)
    dashboard.carteiras = carteiras
}


const saveAcao = (acao) => {
    return new Promise((resolve, reject) => {
        ctrlSaveAcao(acao)
            .then(resp => {
                showToastSuccess(resp.codigo + ' adicionada com sucesso!');
                store.dispatch('addAcao', resp)
                resolve(resp.codigo)
            })
            .catch(error => {
                catchErro(error)
                reject(false)
            })
    })
}

// TODO destrinchar a menssagem function externa
const catchErro = (error) => {
    showToastError(error); // replace em Error: "GraphQL error:
    console.log(error)
    console.log(error.networkError.result.errors[0].message)
}

export {
    init,
    setCarteira,
    saveAcao,
}

/*

   // vue.prototype.$api.resetStore()

    let carteiras = {}
    Object.defineProperty(this, "carteiras", {
        set: function (value) {
            carteiras = value;
            totalGeral = calcTotalGeral(carteiras)
        },
        get: () => {
            return carteiras;
        }
    });



              this.$toast.add({
            severity: "error",
            summary: "Falha ao inserir " + this.novaAcao,
            detail: e.message.replace("GraphQL error:", ""),
            life: 6000
          });



    }    */