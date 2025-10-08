import { mount } from 'svelte';
//import './app.css';
import App from './App.svelte';
// bootstrap
//import './lib/bootstrap-5.3.8-dist/css/bootstrap.min.css';
//import './lib/bootstrap-5.3.8-dist/js/bootstrap.bundle';
// css personalizado 
//import './css/Fijos.css';
const app = mount(App, {
  target: document.getElementById('app')!,
})

export default app
