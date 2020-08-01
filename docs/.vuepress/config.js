const { description } = require('../../package')

module.exports = {
  /**
   * Ref：https://v1.vuepress.vuejs.org/config/#title
   */
  title: 'TIPS',
  /**
   * Ref：https://v1.vuepress.vuejs.org/config/#description
   */
  description: description,

  /**
   * Extra tags to be injected to the page HTML `<head>`
   *
   * ref：https://v1.vuepress.vuejs.org/config/#head
   */
  head: [
    ['meta', { name: 'theme-color', content: '#3eaf7c' }],
    ['meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }],
    ['meta', { name: 'apple-mobile-web-app-status-bar-style', content: 'black' }],
    ['link', { rel: 'icon', href: '/img/favicon.ico' }]
  ],
  
  meta: [
    { charset: 'utf-8' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1' }
  ],

  /**
   * Theme configuration, here is the default theme configuration for VuePress.
   *
   * ref：https://v1.vuepress.vuejs.org/theme/default-theme-config.html
   */

  themeConfig: {
    repo: '',
    logo: '/img/hero.png',
    editLinks: false,
    docsDir: '',
    editLinkText: '',
    lastUpdated: false,
    // displayAllHeaders: true,
    activeHeaderLinks: false,
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Guide', link: '/guide/' },
      { text: 'VuePress', link: 'https://v1.vuepress.vuejs.org' }
    ],
    sidebar: [
      {
        title: 'NLP',
        path: '/nlp/',
        collapsable: true,
        children: [
          ['/nlp/install_tools', '各種ツールのインストール方法']
        ]
      },
      {
        title: 'STATISTICS',
        path: '/statistics/',
        collapsable: true,
        children: [
          '/statistics/descriptive_statistics',
          '/statistics/statistical_hypothesis',
          '/statistics/significance',
          '/statistics/outlie',
          '/statistics/bayesian_statistics',
          ['/statistics/bayesian_estimation', 'ベイズ推定'],
        ],
      },
      {
        title: 'Python',
        path: '/python/',
        collapsable: true,
        children: [
          [ '/python/setup', '環境構築'],
        ]
      },
      {
        title: 'LaTeX',
        path: '/latex/',
        collapsable: true,
      }
    ],
    sidebarDepth: 0,
  },

  /**
   * Advanced Configuration of Markdown-it
   * https://v1.vuepress.vuejs.org/guide/markdown.html#advanced-configuration
   */
  // markdown: {
  //   // options for markdown-it-anchor
  //   anchor: { permalink: false },
  //   // options for markdown-it-toc
  //   toc: { includeLevel: [1, 2] },
  //   extendMarkdown: md => {
  //     // use more markdown-it plugins!
  //     md.use(require('markdown-it-xxx'))
  //   }
  // },

  /**
   * Apply plugins，ref：https://v1.vuepress.vuejs.org/zh/plugin/
   */
  plugins: [
    '@vuepress/plugin-back-to-top',
    '@vuepress/plugin-medium-zoom',
    'vuepress-plugin-latex',    
    'vuepress-plugin-mathjax',
      {
        target: 'svg',
        macros: {
          '*': '\\times',
        },
      },
  ]
}
