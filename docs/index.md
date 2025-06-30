---
layout: home

hero:
  name: "pretty-loguru"
  text: "增強版 Python 日誌庫"
  tagline: "基於 Loguru，集成 Rich 和 ASCII Art，讓日誌輸出更加優雅"
  image:
    src: /logo.png
    alt: pretty-loguru
  actions:
    - theme: brand
      text: 快速開始
      link: /guide/quick-start
    - theme: alt
      text: 查看範例
      link: /examples/
    - theme: alt
      text: GitHub
      link: https://github.com/JonesHong/pretty-loguru

features:
  - icon: 🎨
    title: Rich 區塊日誌
    details: 使用 Rich 面板顯示帶有邊框和樣式的結構化日誌區塊，讓系統狀態一目了然
  - icon: 🎯
    title: ASCII 藝術標題
    details: 使用 art 庫和 pyfiglet 生成引人注目的 ASCII 藝術標題，提升日誌的視覺效果
  - icon: 🔥
    title: 一鍵初始化
    details: 一次呼叫即可同時設置文件和控制台日誌，支援自動輪換和壓縮
  - icon: 🚀
    title: FastAPI 整合
    details: 完美整合 FastAPI 和 Uvicorn，統一 Web 應用的日誌格式和輸出
  - icon: 📊
    title: 預設配置
    details: 提供多種預設配置，包括開發、生產、測試環境的最佳實踐設定
  - icon: 🛠️
    title: 高度自定義
    details: 支援自定義格式、顏色、輪換策略，滿足不同場景的日誌需求
---

## 🚀 快速安裝

```bash
pip install pretty-loguru
```

## ⚡ 超快速開始

```python
from pretty_loguru import logger, logger_start

# 一行代碼初始化日誌系統
component_name = logger_start(folder="my_logs")

# 開始使用各種日誌功能
logger.info("應用程式啟動成功")
logger.success("資料庫連接正常")
logger.warning("記憶體使用率較高")

# Rich 區塊日誌
logger.block(
    "系統狀態摘要",
    [
        "CPU 使用率: 45%",
        "記憶體使用率: 60%", 
        "磁碟空間: 120GB 可用",
        "網路連接: 正常"
    ],
    border_style="green",
    log_level="INFO"
)

# ASCII 藝術標題
logger.ascii_header(
    "SYSTEM READY",
    font="slant",
    border_style="blue"
)
```

## 📸 效果展示

### 基本日誌輸出
![基本範例終端機](/example_1_en_terminal.png)

### Rich 區塊日誌
![Rich 區塊範例](/example_2_en_terminal.png)

### ASCII 藝術標題
![ASCII 藝術範例](/example_3_en_terminal.png)

## 🎯 為什麼選擇 pretty-loguru？

- **🎨 視覺化優先**: 豐富的視覺元素讓日誌不再單調
- **⚡ 開箱即用**: 極簡的 API 設計，幾行代碼即可上手
- **🔧 高度靈活**: 支援多種輸出格式和自定義配置
- **🌐 框架整合**: 完美支援 FastAPI、Uvicorn 等主流框架
- **📦 生產就緒**: 內建日誌輪換、壓縮、清理等企業級功能

## 🚀 下一步

<div class="vp-doc">

- [📖 閱讀完整指南](/guide/) - 了解所有功能和配置選項
- [🎮 查看範例](/examples/) - 從基礎到進階的完整範例
- [🔌 整合指南](/integrations/) - 與 FastAPI、Uvicorn 等框架整合
- [📚 API 文件](/api/) - 詳細的 API 參考文件

</div>

## 📄 授權

本專案採用 [MIT License](https://github.com/JonesHong/pretty-loguru/blob/master/LICENSE) 授權。