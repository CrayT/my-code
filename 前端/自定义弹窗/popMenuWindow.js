(function(window){


    var popMenuWindow = function(title, cancelCallBack, confirmCallBack, options)
    {
        this.createDiv();
        this.$el = document.getElementById('mainMenuWindow')
        this.title = title || "Tips" //标题
        this.canclelButtonText = options.cancelButtonText || null //取消按钮的文字，如果只需要显示一个类似"知道了"的按钮，则不要传改字段
        this.confirmButtonText = options.confirmButtonText || null //确定按钮的文字

        this.input = options.input || false; //是否加入输入框
        this.select = options.select || false; //是否加入下选框
        this.content = options.content || null; //中间显示的内容，数组类型，[{text:内容,style:样式}]，style不必须。

        this.selectList = options.selectList || false; //下选框列表，数组形式
        this.selectContent = null //选择的内容
        this.selectIndex = 0; //选择的索引值
        this.key = options.key || false; //下拉框弹出需要自定义的关键字
        this.keyCallBak = options.keyCallBack || null //执行关键字的回调函数
        this.confirmBtn = $(this.$el).find('.confirm')
        this.cancelBtn = $(this.$el).find('.cancelBtn')
        this.closeBtn = $(this.$el).find('.closeBtn')
        this.selectListShow = options.selectListShow //下拉框在不打开的时候 框中显示的内容，如果不传，则显示列表第一个元素。
        this.showIcon = options.showIcon || false //是否需要显示左上角的感叹号图标
        this.showCloseBtn = options.showCloseBtn || false;
        this.style = options.style || null; //特殊情况自定义样式
        this.additionEvent = options.additionEvent || null //额外事件
        this.init(cancelCallBack, confirmCallBack)
        this.selectOnfire = false; //标识是否选则了下拉列表

        return this;
    }
    popMenuWindow.prototype.bindData = function(key, value){
        this[key] = value;
        return this;
    }
    popMenuWindow.prototype.close = function(){
        $(this.$el).remove();
        $("#popMenuBackground").remove()
    }
    popMenuWindow.prototype.open = function(){
        $(this.$el).show();
        $("#popMenuBackground").show() //打开就显示半透明背景，关闭不关闭
    }
    popMenuWindow.prototype.dispose = function(){
        var self = this;
        self.confirmBtn.off('click')
        self.cancelBtn.off('click')
        if($(self.$el).find(".dropdown-menu").children.length){
            $(self.$el).find(".dropdown-menu").empty()
        }
    }
    popMenuWindow.prototype.createDiv = function(){
        $("body").append(
            '<div id="mainMenuWindow" class="popMenuWindow">' +
            '<div class="closeBtn"><img src="textures/closeUnable.svg"/></div>' +
            '    <div class="title">' +
            '       <img class="hideIcon" src="textures/info.png">' +
            '       <div class="title-content"></div>' +
            '    </div>' +
            '    <div class="contentWindow" >' +
            '    </div>' +
            '    <div id="popMenuDropDown" class="dropdown">' +
            '        <div class="popMenuDropDown selectStyle dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true"><span class="text"></span><img src="textures/phone/dropButton.svg"/></div>' +
            '        <ul class="dropdown-menu ul-phone" id="dropdown-menu"></ul>' +
            '    </div>' +
            '    <div class="input-group" id="input-group">' +
            '        <input class="inputClass" id="inputClass">' +
            '    </div>' +
            '    <div class="btn-new">' +
            '        <div class="cancelBtn" data-i18n-text="cancel">取消</div>' +
            '        <div class="confirmBtn confirm" data-i18n-text="confirm">确定</div>' +
            '    </div>' +
            '</div>');
        $("body").append('<div id="popMenuBackground"></div>')
    }

    popMenuWindow.prototype.init = function(cancelCallBack, confirmCallBack){
        var self = this;

        self.dispose();

        $(self.$el).find(".title > div").text(self.title)

        if(self.showCloseBtn){
            $(self.$el).find(".closeBtn").show();
            $(self.$el).find(".closeBtn").hover(function(){
                $(this).find('img').attr('src', "textures/closeUnable_active.svg")
            }, function(){
                $(this).find('img').attr('src', "textures/closeUnable.svg")
            })
        }
        //执行传入的事件
        if(self.additionEvent){
            eval(self.additionEvent);
        }
        //加载传入的样式
        if(self.style){
            Object.keys(self.style).forEach(function(key){
                $(self.$el).find(key).css(self.style[key])
            })
        }
        if(self.showIcon){
            $(self.$el).find("img").removeClass("hideIcon").addClass("title-img")
            $(self.$el).find(".title").find("div").removeClass("title-content")
            $(self.$el).find(".title").css({"margin-top":"36px"})
        } else {
            if(!checkIsPhone()) {
                $(self.$el).find(".btn-new").css({"margin-right" : "44px", "margin-bottom" : "24px"})
                $(self.$el).find(".title").css({"margin-bottom" : "24px"})
            }
        }
        if(self.canclelButtonText) {
            $(self.$el).find(".cancelBtn").show()
            $(self.$el).find(".cancelBtn").text(self.canclelButtonText)
            $(self.$el).find('.confirm').removeClass('singleConfirmBtn').addClass('confirmBtn')
            $(self.$el).find('.title').find("div").addClass("titleWide");
            $(self.$el).find('.contentWindow').addClass("titleWide");
            $(self.$el).find(".btn-new").css({"position":"relative", "bottom": '0px',"margin-bottom":" 16px"}) //"margin-top":'20px',
            if(checkIsPhone()) {
                $(self.$el).find(".btn-new").css({
                    "margin-top": '20px'
                })
            }
        } else{
            $(self.$el).find(".cancelBtn").hide()
            $(self.$el).find('.confirm').removeClass('confirmBtn').addClass('singleConfirmBtn')
            // $(self.$el).find('.btn-new').css({'position': 'relative'})
            $(self.$el).css({'width': '364px',"min-height": '154px'}) //单独按钮的提示，需要修改整个弹窗的宽高

            if(!checkIsPhone()){
                $(self.$el).find(".btn-new").css("right","48px")
                $(self.$el).find(".contentWindow").css("width","252px")
            } else {
                $(self.$el).find(".contentWindow").css({'width': '300px'})
                $(self.$el).find(".btn-new").css("right","64px")
            }
        }
        if(self.confirmButtonText) {
            $(self.$el).find(".confirm").text(self.confirmButtonText)
        }else{
            $(self.$el).find(".confirm").hide()
        }

        if(self.select){
            $(self.$el).find("#popMenuDropDown").show()
        }else{
            $(self.$el).find("#popMenuDropDown").hide()
        }
        if(self.input){
            $(self.$el).find(".inputClass").val('')
            $(self.$el).find("#input-group").show()
        }else{
            $(self.$el).find("#input-group").hide()
        }
        if(self.content){
            $(self.$el).find(".contentWindow").empty() //每次进来清空内容
            $(self.$el).find(".contentWindow").show()
            self.content.forEach((tip, i) =>{
                let text = tip.text
                let style = "color: black;" + tip.style;
                $(self.$el).find(".contentWindow").append("<div class='contentLetter' style='" + style + "'>" + text + "</div>")
                // $(self.$el).find(".contentWindow").append("<br>")
                if(i < self.content.length - 1) $(self.$el).find(".contentWindow").append("<div style='width:100%;height:12px'></div>") //换行间隔 span若不是block无法设置margin.
            })
            $(self.$el).find(".title").css({
                "margin-bottom": "17px"
            })
            $(self.$el).find(".btn-new").css({
                "margin-bottom": "17px"
            })
        }else{
            $(self.$el).find(".contentWindow").hide()
        }

        //失去焦点 移动端返回菜单返回：
        $(self.$el).find(".inputClass").blur(function(){
            window.scroll(0,0);
        });

        //插入select选择列表
        if(self.select && self.selectList.length > 0 ){ //选择选择框且有列表才展示列表

            let selectBox = document.getElementById('dropdown-menu')
            let htm = "";
            for (let i = 0; i < self.selectList.length; i++) {
                htm = "<li value='" + i + "'>" + self.selectList[i] + "</li>";
                selectBox.innerHTML += "<li value='" + i + "'>" + self.selectList[i] + "</li>";
            }
            self.selectContent = self.selectList[0];
            $(self.$el).find(".dropdown-toggle").find(".text").text(self.selectListShow || self.selectList[0])

            $(self.$el).find(".dropdown>ul>li").click(function() {

                let dom = $("#popMenuDropDown").find(".dropdown-toggle .text");
                if($(this).text() === self.key){ //等于关键字弹出input框
                    $(self.$el).find("#input-group").show()
                    self.input = true
                    self.keyCallBak ? self.keyCallBak() : null;
                }else{
                    $(self.$el).find("#input-group").hide()
                    self.input = false
                }
                self.selectOnfire = true;
                dom.text($(this).text());
                self.selectContent = $(this).text()
                self.selectIndex = self.selectListShow ? this.value - 1 : this.value
            })
        }

        self.cancelBtn.one('click', function(){
            self.close();
            $("#blackBackground").fadeOut();
            cancelCallBack && cancelCallBack()
        })

        self.confirmBtn.one('click', function(){
            var input = null
            var selectContent = null
            var index = 0
            if(self.input){
                input = document.getElementById("inputClass").value
            }
            if(self.select){
                selectContent = $(self.$el).find(".text").text() || self.selectContent;
                let value = Array.from($(self.$el).find(".dropdown-menu").find("li")).filter(r => $(r).text() == selectContent)[0].value;
                //如果没有选则列表项，则匹配当前文本框索引
                index = self.selectOnfire ? self.selectIndex : (self.selectListShow ? value - 1 : value);
            }

            if (input && !selectContent) {
                confirmCallBack && confirmCallBack(input)
                self.close();
                !self.remainBG && $("#blackBackground").fadeOut()
                return
            }
            //有输入，但是输入被清空
            if(self.input && !input){
                confirmCallBack && confirmCallBack('empty')
                self.close();
                !self.remainBG && $("#blackBackground").fadeOut()
                return
            }
            if (!input && selectContent) {
                confirmCallBack && confirmCallBack(selectContent, index)
                self.close();
                !self.remainBG && $("#blackBackground").fadeOut()
                return
            }
            if (input && selectContent) {
                confirmCallBack && confirmCallBack(input, selectContent, index)
                self.close();
                !self.remainBG && $("#blackBackground").fadeOut()
                return
            }
            confirmCallBack && confirmCallBack()
            self.close();
            !self.remainBG && $("#blackBackground").fadeOut()
        })

        self.closeBtn.one('click', function(){
            self.close();
        })
        return self
    }
    window.popMenuWindow = popMenuWindow;
})(window);
