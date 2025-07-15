import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'pretty-loguru',
  description: 'Enhanced Python Logging Library - Based on Loguru, integrated with Rich and ASCII Art',
  
  // GitHub Pages 配置 - 使用 command 來動態設定 base 路徑
  base: process.env.VITE_BASE_PATH || '/pretty-loguru/',
  
  // 暫時忽略死連結檢查，因為文檔還在建構中
  ignoreDeadLinks: true,
  
  head: [
    ['link', { rel: 'icon', href: '/logo.png' }],
    ['meta', { name: 'theme-color', content: '#3c8772' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: 'pretty-loguru' }],
    ['meta', { property: 'og:description', content: 'Enhanced Python Logging Library' }],
  ],

  // i18n settings - moved to top level
  locales: {
    // Chinese (Traditional)
    root: {
      label: '繁體中文',
      lang: 'zh-TW',
      title: 'pretty-loguru',
      description: '增強版 Python 日誌庫 - 基於 Loguru，集成 Rich 和 ASCII Art',
      themeConfig: {
        nav: [
          { text: '首頁', link: '/' },
          { text: '指南', link: '/guide/' },
          { text: '功能', link: '/features/' },
          { text: '整合', link: '/integrations/' },
          { text: '範例', link: '/examples/' },
          { text: 'API', link: '/api/' }
        ],

        sidebar: {
          '/guide/': [
            {
              text: '入門指南',
              items: [
                { text: '簡介', link: '/guide/' },
                { text: '快速開始', link: '/guide/quick-start' },
                { text: '安裝', link: '/guide/installation' },
                { text: '基本用法', link: '/guide/basic-usage' }
              ]
            }
          ],
          '/features/': [
            {
              text: '視覺化功能',
              items: [
                { text: '功能概覽', link: '/features/' },
                { text: 'Rich 區塊日誌', link: '/features/rich-blocks' },
                { text: 'ASCII 藝術標題', link: '/features/ascii-art' },
                { text: 'ASCII 藝術區塊', link: '/features/ascii-blocks' }
              ]
            }
          ],
          '/integrations/': [
            {
              text: '框架整合',
              items: [
                { text: '整合概覽', link: '/integrations/' },
                { text: 'FastAPI 整合', link: '/integrations/fastapi' },
                { text: 'Uvicorn 整合', link: '/integrations/uvicorn' }
              ]
            }
          ],
          '/examples/': [
            {
              text: '範例集合',
              items: [
                { text: '範例總覽', link: '/examples/' },
                { text: '快速開始', link: '/examples/quickstart' },
                { text: '基礎範例', link: '/examples/basics' },
                { text: '視覺化範例', link: '/examples/visual' },
                { text: '配置管理', link: '/examples/configuration' },
                { text: '框架整合', link: '/examples/integrations' },
                { text: '生產環境', link: '/examples/production' },
                { text: '進階用法', link: '/examples/advanced' },
                { text: '企業級應用', link: '/examples/enterprise' }
              ]
            },
            {
              text: '詳細範例',
              items: [
                { text: '控制台 vs 檔案', link: '/examples/basics/console-vs-file' },
                { text: '目標日誌', link: '/examples/basics/target-logging' },
                { text: '簡單用法', link: '/examples/basics/simple-usage' },
                { text: 'ASCII 藝術', link: '/examples/visual/ascii-art' },
                { text: 'Rich 區塊', link: '/examples/visual/blocks' },
                { text: 'Rich 元件', link: '/examples/visual/rich-components' },
                { text: 'FastAPI 詳細整合', link: '/examples/integrations/fastapi-detailed' }
              ]
            }
          ],
          '/api/': [
            {
              text: 'API 參考',
              items: [
                { text: 'API 概覽', link: '/api/' },
                { text: '核心模組', link: '/api/core' },
                { text: '格式化模組', link: '/api/formats' },
                { text: '整合模組', link: '/api/integrations' }
              ]
            }
          ]
        },

        footer: {
          message: '基於 MIT 許可證發布',
          copyright: 'Copyright © 2024 pretty-loguru'
        },

        editLink: {
          pattern: 'https://github.com/JonesHong/pretty-loguru/edit/master/docs/:path',
          text: '在 GitHub 上編輯此頁'
        },

        lastUpdated: {
          text: '最後更新於'
        }
      }
    },

    // English
    en: {
      label: 'English',
      lang: 'en-US',
      title: 'pretty-loguru',
      description: 'Enhanced Python Logging Library - Based on Loguru, integrated with Rich and ASCII Art',
      themeConfig: {
        nav: [
          { text: 'Home', link: '/en/' },
          { text: 'Guide', link: '/en/guide/' },
          { text: 'Features', link: '/en/features/' },
          { text: 'Integrations', link: '/en/integrations/' },
          { text: 'Examples', link: '/en/examples/' },
          { text: 'API', link: '/en/api/' }
        ],

        sidebar: {
          '/en/guide/': [
            {
              text: 'Getting Started',
              items: [
                { text: 'Introduction', link: '/en/guide/' },
                { text: 'Quick Start', link: '/en/guide/quick-start' },
                { text: 'Installation', link: '/en/guide/installation' },
                { text: 'Basic Usage', link: '/en/guide/basic-usage' }
              ]
            }
          ],
          '/en/features/': [
            {
              text: 'Visualization',
              items: [
                { text: 'Overview', link: '/en/features/' },
                { text: 'Rich Blocks', link: '/en/features/rich-blocks' },
                { text: 'ASCII Art Headers', link: '/en/features/ascii-art' },
                { text: 'ASCII Art Blocks', link: '/en/features/ascii-blocks' }
              ]
            }
          ],
          '/en/integrations/': [
            {
              text: 'Framework Integrations',
              items: [
                { text: 'Overview', link: '/en/integrations/' },
                { text: 'FastAPI', link: '/en/integrations/fastapi' },
                { text: 'Uvicorn', link: '/en/integrations/uvicorn' }
              ]
            }
          ],
          '/en/examples/': [
            {
              text: 'Examples',
              items: [
                { text: 'Overview', link: '/en/examples/' },
                { text: 'Quick Start', link: '/en/examples/quickstart' },
                { text: 'Basic Examples', link: '/en/examples/basics' },
                { text: 'Visual Examples', link: '/en/examples/visual' },
                { text: 'Configuration', link: '/en/examples/configuration' },
                { text: 'Integrations', link: '/en/examples/integrations' },
                { text: 'Production', link: '/en/examples/production' },
                { text: 'Advanced', link: '/en/examples/advanced' },
                { text: 'Enterprise', link: '/en/examples/enterprise' }
              ]
            },
            {
              text: 'Detailed Examples',
              items: [
                { text: 'Console vs File', link: '/en/examples/basics/console-vs-file' },
                { text: 'Target Logging', link: '/en/examples/basics/target-logging' },
                { text: 'ASCII Art', link: '/en/examples/visual/ascii-art' },
                { text: 'Rich Blocks', link: '/en/examples/visual/blocks' },
                { text: 'Rich Components', link: '/en/examples/visual/rich-components' },
                { text: 'FastAPI Detailed', link: '/en/examples/integrations/fastapi-detailed' }
              ]
            }
          ],
          '/en/api/': [
            {
              text: 'API Reference',
              items: [
                { text: 'Overview', link: '/en/api/' },
                { text: 'Core Modules', link: '/en/api/core' },
                { text: 'Formatting Modules', link: '/en/api/formats' },
                { text: 'Integration Modules', link: '/en/api/integrations' }
              ]
            }
          ]
        },

        footer: {
          message: 'Released under the MIT License.',
          copyright: 'Copyright © 2024 pretty-loguru'
        },

        editLink: {
          pattern: 'https://github.com/JonesHong/pretty-loguru/edit/master/docs/:path',
          text: 'Edit this page on GitHub'
        },

        lastUpdated: {
          text: 'Last Updated'
        }
      }
    }
  },

  themeConfig: {
    logo: '/logo.png',
    
    socialLinks: [
      { icon: 'github', link: 'https://github.com/JonesHong/pretty-loguru' }
    ],

    search: {
      provider: 'local',
      options: {
        locales: {
          'root': {
            translations: {
              button: {
                buttonText: '搜尋文件',
                buttonAriaLabel: '搜尋文件'
              },
              modal: {
                noResultsText: '無法找到相關結果',
                resetButtonTitle: '清除查詢條件',
                footer: {
                  selectText: '選擇',
                  navigateText: '切換'
                }
              }
            }
          },
          'en': {
            translations: {
              button: {
                buttonText: 'Search Documentation',
                buttonAriaLabel: 'Search Documentation'
              },
              modal: {
                noResultsText: 'No results found',
                resetButtonTitle: 'Reset search',
                footer: {
                  selectText: 'to select',
                  navigateText: 'to navigate'
                }
              }
            }
          }
        }
      }
    }
  }
})