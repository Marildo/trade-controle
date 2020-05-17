import { loadTipoLancamentos } from "@/controllers/tiposLancamentosController"
import {loadAcoes} from "@/controllers/acaoController"
import {loadCarteiras} from "@/controllers/carteiraController"

const init = () =>{
    loadCarteiras()
    loadAcoes()
    loadTipoLancamentos()
}

export { init}