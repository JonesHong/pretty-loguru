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
from pretty_loguru import create_logger

# 一行代碼初始化日誌系統
logger = create_logger(
    name="docs_demo",
    log_path="my_logs",
    level="INFO"
)

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

## 🧭 **我該從哪裡開始？**

### 📊 根據您的身份選擇

| 我是... | 建議路徑 | 預估時間 |
|---------|----------|----------|
| 🆕 **Python 日誌新手** | [5分鐘體驗](/examples/) → [核心功能](/examples/) → [視覺化](/examples/) | 30分鐘 |
| 🌐 **Web 開發者** | [快速開始](/guide/quick-start) → [核心功能](/examples/) → [框架整合](/integrations/) | 45分鐘 |
| 🏭 **DevOps/運維** | [安裝配置](/guide/installation) → [生產實踐](/examples/) → [進階配置](/examples/) | 1小時 |
| 🔬 **進階開發者** | [API文件](/api/) → [完整範例](/examples/) → [自定義開發](/examples/) | 2-3小時 |

### 🎯 根據您的需求選擇

<div class="vp-doc">

| 我想要... | 直接跳到 |
|-----------|----------|
| ⚡ **5分鐘快速體驗** | [快速體驗](/examples/) |
| 🎨 **美化日誌輸出** | [視覺化功能](/examples/) |
| 🚀 **FastAPI 整合** | [框架整合](/integrations/) |
| 🏭 **生產環境部署** | [生產實踐](/examples/) |
| 📚 **完整學習** | [學習中心](/examples/) |

</div>

## 🚀 學習路徑

<div class="vp-doc">

- [🚀 5分鐘快速體驗](/examples/) - 立即感受 pretty-loguru 的魅力
- [📚 核心功能掌握](/examples/) - 掌握所有基礎功能
- [🎨 視覺化功能](/examples/) - Rich 區塊和 ASCII 藝術
- [⚙️ 配置和管理](/examples/) - 檔案輪替和進階配置
- [🌐 框架整合](/integrations/) - FastAPI、Uvicorn 整合
- [🏭 生產環境](/examples/) - 企業級部署和維運
- [📚 API 參考](/api/) - 完整的函數說明文件

</div>

## 📄 授權

本專案採用 [MIT License](https://github.com/JonesHong/pretty-loguru/blob/master/LICENSE) 授權。