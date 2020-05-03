import Vue from 'vue';
import Vuetify from 'vuetify/lib'
import VCurrencyField from 'v-currency-field'
import { VTextField } from 'vuetify/lib'  //Globally import VTextField

import '@fortawesome/fontawesome-free/css/all.css' 

Vue.use(Vuetify);
Vue.component('v-text-field', VTextField)
Vue.use(VCurrencyField, { 
	locale: 'pt-BR',
	decimalLength: 2,
	autoDecimalMode: true,
	min: null,
	max: null,
	defaultValue: 0
})


export default new Vuetify({
	icons: {
		iconfont: 'fa',
	}
});
