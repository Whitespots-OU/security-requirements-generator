module.exports = {
  outputDir: process.env.NODE_ENV === 'production' ? 'dist/prod' : 'dist/dev',
  publicPath: '/',
  lintOnSave: false,
  runtimeCompiler: true,
  chainWebpack: config => {
    config
        .plugin('html')
        .tap(args => {
          args[0].title = 'Security Requirements - Whitespots';
          return args;
        });
  },
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure:false,
        pathRewrite: {'^/api': '/api'},
        logLevel: 'debug'
      },
      '^/media': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure:false,
        pathRewrite: {'^/media': '/media'},
        logLevel: 'debug'
      },
    }
  }
}
