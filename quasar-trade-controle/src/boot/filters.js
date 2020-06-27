import { formaterReal } from '../utils/numberUtils'

export default ({ Vue }) => {
  Vue.filter('formaterReal', (value) => formaterReal(value))
}
