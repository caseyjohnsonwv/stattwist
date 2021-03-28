import Vue from 'vue';
import VueSession from 'vue-session';
import VueCookie from 'vue-cookie';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faRetweet, faHeart } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.css';

Vue.config.productionTip = false;
Vue.use(VueSession);
Vue.use(VueCookie);

library.add(faRetweet);
library.add(faHeart);
Vue.component('font-awesome-icon', FontAwesomeIcon);

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
