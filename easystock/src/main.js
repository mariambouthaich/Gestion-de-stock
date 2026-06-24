import { createApp } from 'vue'
import App from './App.vue'
import { makeRouter } from './router/index.js'
import './styles.css'

const app = createApp(App)
app.use(makeRouter())
app.mount('#app')
