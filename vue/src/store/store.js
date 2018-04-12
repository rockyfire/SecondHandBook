//引入vue
import Vue from 'vue'
//全局引入vueX
import Vuex from 'vuex';

import mutations from './mutations';
import * as actions from './actions';
import * as getters from './getters';

//全局注册vueX
Vue.use(Vuex);
//全局引用cookie方法类
import cookie from '../static/js/cookie';

const userInfo = {
            name:cookie.getCookie('name')||'',
            token:cookie.getCookie('token')||''
        };
const books_list =  {
       totalPrice:'',
        books_list:[]

    }
const state = {
    userInfo,
    books_list
}
export default new Vuex.Store({
	state,
	mutations,
	actions,
	getters
});


// const store = new Vuex.Store({
//   state: {
//     authority:''
//   },
//   mutations: {
//     setAuthority(){
//         state.authority = JSON.parse(cookie.getCookie('authority')); 
//     }

//   }
// })

// export default store;



