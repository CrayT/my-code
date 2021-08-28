/**
 * 这是个强大消息提示框工具
 * @param msg
 * @param config
 * config.duration 停顿秒数
 * config.style 风格 black: 黑色（默认） white: 白色
 * config.pos middle top bottom
 * config.icon success error warning ask hello, 或者指定图片路径
 * config.zIndex 层级， 默认是999999
 * config.animate animate.css动画
 */
(function ($) {
    // html template
    var _template = '' +
        '<div id="_hintMsg" class="_hintMsg animated" style="display:flex;min-height: 44px;width:fit-content;border-radius: 8px;position: absolute;">' +
        '    <div class="icon" style="line-height: 44px;margin:0 10px 0 18px"><img height="24px" style="vertical-align: middle" src=""></div>' +
        '    <div class="msg" style="vertical-align: middle;margin: 0 18px 0 0;line-height: 44px;white-space: nowrap;overflow: hidden;text-overflow: ellipsis;font-size: 14px;"></div>' +
        '</div>';
    // 风格
    var _styles = {
        'black': {
            color: "#fff",
            background: "#333"
        },
        'white': {
            color: "#333",
            background: "#fff"
        }
    };
    // 默认初始化配置
    var _config = {
        duration: 3,
        style: 'black',
        pos: 'bottom',
        icon: "", // 默认不带icon
        zIndex: 999999,
        animation: "fadeIn",
        icon:"./textures/markPoint/dragLineHint.png"
    };

    // 默认icon配置 todo elvis
    var _icons = {
        'success': "",
        'error': "",
        'warning': "",
        'ask': "",
        'hello': "",
    }

    $.msg = function (msg, config, callBack) {
        let tempClone = $(_template).clone().attr('id', '_hintMsg_' + Date.now());
        let mergedConfig = $.extend({}, _config, config);
        // 指定主题风格
        if(typeof mergedConfig.style === 'object') {
            tempClone.css(mergedConfig.style)
        } else {
            tempClone.css(_styles[mergedConfig.style]);
        }

        if(mergedConfig.isHtml){
            tempClone.find('.msg').append(msg);
        } else {
            tempClone.find('.msg').text(msg);
        }
        // icon
        if (mergedConfig.icon === "" || mergedConfig.icon === null) {
            tempClone.find('.icon').remove();
            tempClone.find('.msg').css({
                width: '100%',
                marginLeft: '20px',
            });
        } else if (typeof mergedConfig.icon === 'string') {
            // 预留的配置
            if (Object.keys(_icons).includes( mergedConfig.icon )) {
                tempClone.find('.icon>img').attr("src", "data:image/png;base64," + _icons[mergedConfig.icon]);
            } else {
                tempClone.find('.icon>img').attr("src", mergedConfig.icon);
            }
        }
        // pos
        if (mergedConfig.pos === 'bottom' || mergedConfig.pos === 'b') {
            tempClone.css("bottom", "115px");
        } else if (mergedConfig.pos === 'middle' || mergedConfig.pos === 'm') {
            tempClone.css({"top": "50%", "transform": "translate(-50%, -50%)"});
        } else if (mergedConfig.pos === 'top' || mergedConfig.pos === 't') {
            tempClone.css("top", "60px");
        } else if (typeof mergedConfig.pos === 'object') {
            tempClone.css(mergedConfig.pos);
        }

        if(!mergedConfig.notCenter){//当弹窗不需要居中时，增加参数控制，防止left和right发生冲突
            tempClone.css('left', '50%')
            tempClone.css('transform', 'translateX(-50%)')
        }

        // zIndex
        tempClone.css('zIndex', mergedConfig.zIndex);

        // animate
        tempClone.addClass(mergedConfig.animation);

        tempClone.appendTo(document.body);

        tempClone.show(null, null, function(){
            if(callBack){
                eval(callBack)
            }
        });

        // duration
        if (mergedConfig.duration) {
            setTimeout(function () {
                tempClone.remove();
            }, parseInt(mergedConfig.duration) * 1000);
        }

    }

})(jQuery);
