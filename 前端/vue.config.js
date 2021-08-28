const path = require('path')
const webpackCustomerConfig = require('./public/config');
const CopyWebpack = require('copy-webpack-plugin')
const {getVersions} = require('./build/sdk.versions');

const isDev = process.env.NODE_ENV === 'development';
const sdkVersions = getVersions(isDev);
const utils = require('./build/utils');

const version =  utils.formatDate(new Date());
console.log('version:\n'+version)
console.log('sdkVersions:\n',sdkVersions)

const convert = function(){
  return 'window.Config=' + JSON.stringify(webpackCustomerConfig)
}
const generateSDKScripts = function(){
  const prefix = isDev ? '/' : '';
  return `
      <script src=${prefix}config.js></script>
      <script src=${prefix}static/js/sdk/three@0.126.1.min.js></script>
      <script src=${prefix}static/js/sdk/panocore@2020122401.min.js></script>
      <script src=${prefix}static/js/sdk/vrstudio@${version}.min.js></script>
    `
}
module.exports = {
  publicPath: isDev ? '/' : './',
  assetsDir:'static',
  indexPath:'index.html',
  filenameHashing: true,
  productionSourceMap: false,
  chainWebpack:config =>{
    config.plugin('copy').use(CopyWebpack).tap(op => {
      if ( !Array.isArray( op[0] )) {
        op[0] = [];
      }
      op[0].push(...utils.getSdkFiles(sdkVersions));
      //Config配置
      op[0].push({
        from: path.resolve(__dirname, './public/config.js'),
        to: path.resolve(__dirname, './dist/'),
        transform: function (content) {
          return convert(content)
        }
      })
      //textures
      op[0].push({
        from: path.resolve(__dirname, './src/assets/sdk-textures/'),
        to: path.resolve(__dirname, './dist/static/sdkTextures/'),
        toType: 'dir'
      })
      return op
    })
    config.plugin('html').tap(op =>{
        op[0].title = '123看房：中国唯一能用于海量二手房的VR远程看房、3D建模和在线家装平台';
        op[0].para = {
          'sdkScripts': generateSDKScripts()
        }
        return op
    })
  },

  devServer:{
    port:1112
  },
  css: {
    // Enable CSS source maps.
    sourceMap: isDev ? true : false,
  },
  lintOnSave:false //关闭eslint检查
}
