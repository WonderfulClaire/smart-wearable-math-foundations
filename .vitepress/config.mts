
import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  title: '智能穿戴设备的数学基础',
  titleTemplate: ':title · 智能穿戴设备的数学基础',
  description: '从真实穿戴设备问题出发，学习矩阵分析、随机过程、凸优化与统计学习。',
  base: '/smart-wearable-math-foundations/',
  cleanUrls: true,
  lastUpdated: true,
  srcExclude: [
    '**/README.md',
    'README_en.md',
    '.github/**',
    'node_modules/**'
  ],
  markdown: {
    math: true,
    lineNumbers: true,
    image: {
      lazyLoad: true
    }
  },
  themeConfig: {
    logo: '/assets/note-framework.svg',
    outline: {
      level: [2, 3],
      label: '本页目录'
    },
    nav: [
      { text: '开始学习', link: '/01-矩阵分析/' },
      { text: '学习路线', link: '/docs/学习路线' },
      { text: '立项计划', link: '/DATAWHALE_PLAN' },
      {
        text: 'GitHub',
        link: 'https://github.com/WonderfulClaire/smart-wearable-math-foundations'
      }
    ],
    sidebar: [
      {
        text: '项目导读',
        items: [
          { text: '首页', link: '/' },
          { text: '八周学习路线', link: '/docs/学习路线' },
          { text: 'Datawhale 立项计划', link: '/DATAWHALE_PLAN' },
          { text: '立项申请草案', link: '/DATAWHALE_APPLICATION' },
          { text: '引用与版权', link: '/docs/引用与版权说明' },
          { text: '内测方案', link: '/docs/内测方案' }
        ]
      },
      {
        text: '01 矩阵分析',
        collapsed: false,
        items: [
          { text: '知识地图', link: '/01-矩阵分析/' },
          {
            text: '多通道复数向量',
            link: '/01-矩阵分析/01-多通道复数向量与-Hermitian-结构'
          },
          {
            text: '协方差与 MVDR',
            link: '/01-矩阵分析/02-协方差矩阵、二次型与-MVDR'
          },
          {
            text: 'SVD 与低秩结构',
            link: '/01-矩阵分析/03-特征分解、SVD-与低秩结构'
          }
        ]
      },
      {
        text: '02 随机过程',
        items: [
          { text: '知识地图', link: '/02-随机过程/' },
          {
            text: '平稳性、自相关与 PSD',
            link: '/02-随机过程/01-平稳性、自相关与-PSD'
          }
        ]
      },
      {
        text: '03 凸优化',
        items: [
          { text: '知识地图', link: '/03-凸优化/' }
        ]
      },
      {
        text: '04 统计学习理论',
        items: [
          { text: '知识地图', link: '/04-统计学习理论/' }
        ]
      }
    ],
    search: {
      provider: 'local'
    },
    lastUpdated: {
      text: '最后更新'
    },
    docFooter: {
      prev: '上一篇',
      next: '下一篇'
    },
    footer: {
      message: '内容与代码采用 MIT License',
      copyright: 'Copyright © WonderfulClaire and contributors'
    },
    socialLinks: [
      {
        icon: 'github',
        link: 'https://github.com/WonderfulClaire/smart-wearable-math-foundations'
      }
    ]
  }
})
