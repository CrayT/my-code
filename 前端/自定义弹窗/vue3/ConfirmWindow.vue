<template>
  <div id="mainMenuWindow" class="popMenuWindow" :class="{mainBoxClassV2: !cancelButtonText}">
      <div class="closeBtn"><img src="../../assets/textures/closeUnable.svg"/></div>
      <div class="title" :class="{titleV2: showIcon}">
           <img src="../../assets/textures/info.png" :class="{hideIcon: !showIcon, 'title-img': showIcon}">
           <div :class="{'title-content': !showIcon, 'titleWide' : cancelButtonText}">{{title}}</div>
        </div>
      <div class="contentWindow" v-show="content" :class="{'titleWide' : cancelButtonText}">
        <div v-for="(item, index) in content">
          {{item.text}}
        </div>
      </div>
      <div id="popMenuDropDown" class="dropdown" v-if="select">
            <div class="popMenuDropDown selectStyle dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
              <span class="text"></span><img src="../../assets/textures/phone/dropButton.svg"/>
            </div>
            <ul class="dropdown-menu ul-phone" id="dropdown-menu"></ul>
        </div>
      <div class="input-group" id="input-group">
            <input class="inputClass" id="inputClass">
      </div>
      <div class="btn-new" :class="{'btn-new-addition': cancelButtonText, 'btn-new-right': !cancelButtonText}">
            <div class="cancelBtn" @click="cancel" v-if="cancelButtonText">{{cancelText}}</div>
            <div class="confirm" @click="confirm" :class="{'singleConfirmBtn': !cancelButtonText, 'confirmBtn': cancelButtonText}">{{confirmText}}</div>
      </div>
  </div>
  <div class="popMenuBackground"></div>
</template>

<script>
import locale from "@/mixins/locale";
export default {
  name: "ConfirmWindow",
  mixins : [locale],
  data(){
    return {
      selectOnfire: false,
      confirmBtn: null,
      cancelBtn: null,
      closeBtn:  null
    }
  },
  props:{
    title:{
      type: String,
      default: 'Tips'
    },
    cancelButtonText: {
      type: String,
      default: null
    },
    confirmButtonText:{
      type: String,
      default: null
    },
    input:{
      type: Boolean,
      default: false
    },
    select:{
      type: Boolean,
      default: false
    },
    content:{
      type: Array,
      default: null
    },
    selectList:{
      type: Array,
      default: null
    },
    selectContent:{
      type: String,
      default: null
    },
    selectIndex:{
      type: Number,
      default: 0
    },
    key:{
      type: String,
      default: null
    },
    keyCallBak:{
      type: Function,
      default: null
    },
    selectListShow:{
      type: String,
      default: null
    },
    showIcon:{
      type: Boolean,
      default: false
    },
    showCloseBtn:{
      type: Boolean,
      default: false
    },
    style:{
      type: Object,
      default: null
    },
    additionEvent:{
      type: String,
      default: null
    },
    onCancel:{
      type: Function,
      default: null
    },
    onConfirm:{
      type: Function,
      default: null
    }
  },
  methods:{
    init(){

    },
    //取消
    cancel(){
      this.onCancel && this.onCancel();
      this.close();
    },
    //关闭弹窗
    close(){
      this.$attrs.remove();
    },
    //确认
    confirm(){
      this.onConfirm && this.onConfirm();
      this.close();
    }
  },
  setup(props, context){


  },
  mounted() {

  },
  computed:{
    confirmText(){
      return this.confirmButtonText || this.t("confirm")
    },
    cancelText(){
      return this.cancelButtonText || this.t("cancel")
    },
  }
}
</script>

<style scoped>
@import "../../assets/css/popMenuWindowPC.css";
.mainBoxClassV2{
  width: 364px;
  min-height: 154px
}
.titleV2{
  margin-top: 36px!important;
}
.popMenuBackground {
  position: absolute;
  z-index: 999;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,.3);
}
.btn-new-addition{
  position: relative;
  buttom:0px;
  margin-bottom: 16px;
}
.btn-new-right{
  right:48px
}
</style>
