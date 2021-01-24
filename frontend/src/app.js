import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios'

import store from './store/index.js';

import MainContainer from './components/Main.vue';


// Enable plugins
Vue.use(VueAxios, axios)

axios.interceptors.request.use((config) => {
    // Push csrf token to axios header
    // This is not reactive, if token is updated from further forms, it won't
    // be bubbled up to axios header
    config.headers['X-CSRFToken'] = vm.$cookie.get('csrftoken');

    return config
});


// Start main app
var vm = new Vue({
    el: '#app',
    store,
    render: h => h(MainContainer)
});
