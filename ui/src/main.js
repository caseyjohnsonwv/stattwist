import Vue from 'vue';
import VueSession from 'vue-session';
import VueCookie from 'vue-cookie';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.css';

Vue.config.productionTip = false;
Vue.use(VueSession);
Vue.use(VueCookie);

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
