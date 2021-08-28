/**
 * 制作端自定义弹窗组件，相应vue组件為ConfirmWindow.
 CreateDate:20210418.
 */
import { createApp } from 'vue';
import ConfirmWindow from "@/components/commonComponents/ConfirmWindow";
import lang from "@/i18n/index";
import {createI18n} from "vue-i18n";

let createMount = (opts) => {
  const mountNode = document.createElement('div');
  document.body.appendChild(mountNode);

  const app = createApp(ConfirmWindow, {
    ...opts,
    remove() {
      app.unmount(mountNode);
      document.body.removeChild(mountNode);
    }
  })
  const i18n = createI18n({
    locale: 'zh-CN',
    messages: lang
  })
  app.use(i18n);
  return app.mount(mountNode)
}

function popUpWindow(options = {}) {
  let inst = createMount(options);
  return inst
}
popUpWindow.install = app => {
  app.config.globalProperties.$confirm = popUpWindow;
}
export default popUpWindow;
