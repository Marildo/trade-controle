import store from './../store/';

import CarteiraController from "./carteiraController";
import AcaoController from "./acaoController"

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

const loadAcoes = () => {
    new AcaoController().loadAcoes()
        .then(resp => store.commit('setAcoes', resp.data.acoes))
        .catch(error => {
            console.log(error)
            console.log(error.networkError.result.errors)
        })
}


function init() {
    loadCarteiras()
    loadAcoes()
}

function setCarteira(carteira) {
    const dashboard = store.getters.dashboard
    const index = dashboard.carteiras.findIndex(i => i.id == carteira.id)
    const carteiras = dashboard.carteiras.splice(index, 1, carteira)
    dashboard.carteiras = carteiras
}

export {
    init,
    setCarteira
}

/*
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
    */