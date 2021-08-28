import { createApp } from 'vue'
import App from './App.vue'
import {createI18n} from "vue-i18n";
import lang from "../src/i18n/index";
import store from "@/store";
import EventBus from "@/eventBus";
// import axios from "axios";
import kfmsg from "@/plugin/KfMsg";
import ConfirmWindow from "@/plugin/ConfirmWindow";
const i18n = createI18n({
    locale: 'zh-CN',
    messages: lang
})
const app = createApp(App)
app.use(i18n);
app.use(store);
app.use(new kfmsg)
app.use(ConfirmWindow)
// app.use(axios); //会报错
app.config.globalProperties.$bus = new EventBus()
app.mount('#app')
