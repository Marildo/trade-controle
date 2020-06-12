import vue from 'vue'

const sucessMessage = (message, caption) => {
  vue.prototype.$q.notify({
    color: 'green-4',
    textColor: 'white',
    icon: 'cloud_done',
    position: 'top',
    message,
    caption
  })
}

const errorMessage = (message, caption) => {
  vue.prototype.$q.notify({
    color: 'red-4',
    textColor: 'white',
    icon: 'cloud_done',
    position: 'top',
    message,
    caption
  })
}

export {
  sucessMessage,
  errorMessage
}
