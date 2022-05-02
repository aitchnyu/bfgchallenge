import axios from "axios";
import Vue from "vue";

import App from "./App.vue";

Vue.config.productionTip = false;

/**
 * Config global for axios/django
 */
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";

new Vue({
  render: (h) => h(App),
}).$mount("#app");
