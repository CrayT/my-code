## 环境要求
- 安装有Linux源码编译环境`build-essential`包

## 安装rvm

```bash
gpg --keyserver hkp://pgp.mit.edu --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
curl -sSL https://get.rvm.io | bash -s stable
source ~/.rvm/scripts/rvm

#若使用zsh
tee -a ~/.zshrc << EOF
[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" 
EOF

#若使用bash
tee -a ~/.bashrc << EOF
[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" 
EOF
```

## 安装ruby

```bash
# 修改rvm工具的ruby源码获取地址为云平台ruby源
echo "ruby_url=https://mirrors.dlcloud.info/ruby/ruby" > ~/.rvm/user/db

# 使用rvm从源码编译安装ruby
rvm install ruby --disable-binary

# 打印安装的ruby版本
ruby -v
```

## 配置rubygems源

```bash
# 列举当前的rubygems源
gem sources  

# 移除默认的官方源并添加云平台rubygems源
gem sources --remove https://rubygems.org/  
gem sources -a https://mirrors.dlcloud.info/rubygems/ 

# 更新gem工具，并打印当前使用的gem版本
gem update --system
gem -v

# 可选，使用gem工具安装bunlder、rails，并将bunlder工具的源也配置为云平台rubygems源
gem install bundler rails
bundle config mirror.https://rubygems.org https://mirrors.dlcloud.info/rubygems/
``` 