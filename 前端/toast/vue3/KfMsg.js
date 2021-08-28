/**
 * 封装toast弹窗插件
 CreateDate:20210407.
 */
const kfmsg = function(){
  this._template = '' +
    '<div id="_hintMsg" class="animated" style="display:flex;min-height: 44px;width:fit-content;border-radius: 8px;position: absolute;">' +
    '    <div class="icon" style="line-height: 44px;margin:0 10px 0 18px"><img height="24px" style="vertical-align: middle" src=""></div>' +
    '    <div class="msg" style="vertical-align: middle;margin: 0 18px 0 0;line-height: 44px;white-space: nowrap;overflow: hidden;text-overflow: ellipsis;font-size: 14px;"></div>' +
    '</div>';
  // 风格
  this._styles = {
    'black': {
      color: '#fff',
      background: '#333'
    },
    'white': {
      color: '#333',
      background: '#fff'
    }
  };
  // 默认初始化配置
  this._config = {
    duration: 3,
    style: 'black',
    pos: 'bottom',
    zIndex: 999999,
    animation: 'fadeIn',
    icon: 'warning'
  };

  // 默认icon配置 todo elvis
  this._icons = {
    'success': '',
    'error': '',
    'warning': 'data:image/png;base64,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',
    'ask': '',
    'hello': ''
  };
}
kfmsg.prototype.install = function install (app, injectKey) {
  app.provide(injectKey);
  app.config.globalProperties.$msg = this;
};
kfmsg.prototype.test = function(){
  console.log('testMsg')
}

kfmsg.prototype.setStyle =function(dom, style, styleVal) {
    if (typeof style === 'object') {
      for (let styleName in style) {
        dom.style[styleName] = style[styleName]
      }
    }
    if (typeof style === 'string' && typeof styleVal === 'string') {
      dom.style[style] = styleVal
    }
  };

kfmsg.prototype.clearAllMsg = function() {
    document.querySelectorAll('div[id^="_hintMsg_"]').forEach(e => e.remove())
  }

  /** 展示提示框
   * @param msg String类型，提示框内要显示的信息
   * @param config Object类型，用户自定义设置信息，会与默认配置 this._config 合并（自定义覆盖默认）
   * <br>config 的键（没有被'包起来）如下<br>
   * duration: 值为 number 类型，提示框持续时间，单位秒，默认3,<br>
   * style: 值为 String 或者 Object 类型，提示框风格，目前支持 'black' 和 'white’ 两种预设风格，默认 'black',<br>
   * pos: 值为 String 类型，提示框出现的位置，目前支持 'bottom','middle','top' 三种，默认 'bottom',<br>
   * zIndex: 值为 number 类型，提示框层级，值越高，在网页中就越优先显示（对应 css 的 z-index），默认999999,<br>
   * animation: 值为 String 类型，'fadeIn',<br>
   * icon: 值为 String 类型，提示框图标，默认 'warning'<br>
   */
kfmsg.prototype.showMsg = function(msg, config) {
    let wrapDiv = document.createElement('div')
    wrapDiv.innerHTML = this._template
    let tempClone = wrapDiv.children[0]
    tempClone.setAttribute('id', '_hintMsg_' + Date.now())
    let mergedConfig = Object.assign({}, this._config, config)
    // 指定主题风格
    if (typeof mergedConfig.style === 'object') {
      this.setStyle(tempClone, mergedConfig.style)
    } else {
      this.setStyle(tempClone, this._styles[mergedConfig.style])
    }
    let msgNode = tempClone.children[1]
    msgNode.innerText = msg
    // icon
    let iconNode = tempClone.children[0]
    let iconImgNode = iconNode.children[0]
    if (mergedConfig.icon === '' || mergedConfig.icon === null) {
      this.setStyle(iconNode, 'display', 'none')
      this.setStyle(msgNode, {
        width: '100%',
        marginLeft: '20px'
      })
    } else if (typeof mergedConfig.icon === 'string') {
      // 预留的配置
      if (Object.keys(this._icons).includes(mergedConfig.icon)) {
        iconImgNode.src = this._icons[mergedConfig.icon]
      } else {
        iconImgNode.src = mergedConfig.icon
      }
    }
    // pos
    if (mergedConfig.pos === 'bottom' || mergedConfig.pos === 'b') {
      this.setStyle(tempClone, 'bottom', '115px')
    } else if (mergedConfig.pos === 'middle' || mergedConfig.pos === 'm') {
      this.setStyle(tempClone, {'top': '50%', 'transform': 'translate(-50%, -50%)'})
    } else if (mergedConfig.pos === 'top' || mergedConfig.pos === 't') {
      this.setStyle(tempClone, 'top', '60px')
    } else if (typeof mergedConfig.pos === 'object') {
      this.setStyle(tempClone, mergedConfig.pos)
    }

    if (!mergedConfig.notCenter) { // 当弹窗不需要居中时，增加参数控制，防止left和right发生冲突
      this.setStyle(tempClone, {
        left: '50%',
        transform: 'translateX(-50%)'
      })
    }

    // zIndex
    this.setStyle(tempClone, 'zIndex', mergedConfig.zIndex)

    // animate
    tempClone.classList.add(mergedConfig.animation)

    document.body.appendChild(tempClone)

    // duration
    if (mergedConfig.duration > 0) {
      setTimeout(function () {
        document.body.removeChild(tempClone)
      }, parseInt(mergedConfig.duration) * 1000)
    }
  }

export default kfmsg;
