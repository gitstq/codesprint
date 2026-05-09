<!-- Multi-language README for CodeSprint -->

<p align="center">
  <a href="#english">English</a> •
  <a href="#简体中文">简体中文</a> •
  <a href="#繁體中文">繁體中文</a>
</p>

---

<a name="english"></a>
# 🚀 CodeSprint

<div align="center">

**Lightweight Multi-Language Code Snippet Intelligent Runner CLI**

*Zero Dependencies • Auto Language Detection • Sandbox Execution • Beautiful TUI Output*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

---

## 🎉 Introduction

**CodeSprint** is a lightweight, zero-dependency CLI tool that lets you **run code snippets in 18+ programming languages** directly from your terminal. No more switching between different IDEs or installing heavy-weight tools - just write and run!

### Why CodeSprint?

- ❌ **Tired of** switching between different IDEs for different languages?
- ❌ **Frustrated with** heavy-weight tools just to test a simple snippet?
- ❌ **Annoyed by** complex setup processes for code playgrounds?

**CodeSprint solves all these problems!** ✅

### 🌟 Key Features

| Feature | Description |
|---------|-------------|
| 🔍 **Auto Language Detection** | Automatically detects language from file extension, shebang, or code patterns |
| 🚀 **18+ Languages** | Python, JavaScript, TypeScript, Go, Rust, Java, C, C++, Ruby, PHP, Bash, Perl, Lua, R, Kotlin, Swift, Scala, and more |
| 🔒 **Sandbox Execution** | Safe, isolated execution with timeout protection |
| 📊 **Beautiful TUI Output** | Colorful, syntax-highlighted output with execution statistics |
| 📚 **History Management** | Track all executions, mark favorites, search and export |
| 💻 **Interactive REPL Mode** | Quick code testing in an interactive environment |
| 🔄 **Batch Execution** | Run multiple files or code snippets at once |
| ⚡ **Zero Dependencies** | Pure Python, no external dependencies required |

---

## 🚀 Quick Start

### Requirements

- Python 3.8 or higher
- Language runtimes for the languages you want to execute (e.g., `node` for JavaScript, `go` for Go)

### Installation

```bash
# Install from PyPI
pip install codesprint

# Or install from source
git clone https://github.com/gitstq/codesprint.git
cd codesprint
pip install -e .
```

### Basic Usage

```bash
# Run a file
codesprint script.py

# Run inline code
codesprint -c "print('Hello, World!')"

# Specify language explicitly
codesprint -l javascript -c "console.log('Hello!')"

# Interactive mode
codesprint -i

# List available runtimes
codesprint -L
```

---

## 📖 Detailed Usage Guide

### Running Files

```bash
# Run Python file
codesprint main.py

# Run JavaScript file
codesprint app.js

# Run Go file
codesprint main.go

# Run with custom timeout (seconds)
codesprint --timeout 60 slow_script.py
```

### Inline Code Execution

```bash
# Python
codesprint -c "import sys; print(sys.version)"

# JavaScript
codesprint -l js -c "console.log(process.version)"

# Ruby
codesprint -l ruby -c "puts RUBY_VERSION"
```

### Interactive REPL Mode

```bash
codesprint -i
```

```
🚀 CodeSprint Interactive Mode
════════════════════════════════════════════════════════════════
Type code and press Enter to execute. Type 'exit' or 'quit' to exit.

>>> print('Hello, World!')

✅ SUCCESS  PYTHON  ⏱ 0.012s
──────────────────────────────────────────────────

📤 Output:
  Hello, World!
```

### History Management

```bash
# Show history
codesprint -H

# Show statistics
codesprint -s

# Clear history
codesprint --clear-history
```

### JSON Output (for scripting)

```bash
codesprint --json -c "print('hello')"
```

```json
{
  "success": true,
  "output": "hello\n",
  "error": "",
  "exit_code": 0,
  "execution_time": 0.015,
  "language": "python"
}
```

---

## 💡 Design Philosophy & Roadmap

### Design Philosophy

CodeSprint was built with these principles in mind:

1. **Zero Dependencies** - No external dependencies means faster installation and fewer conflicts
2. **Security First** - Sandbox execution with timeout protection prevents runaway code
3. **Developer Experience** - Beautiful output, helpful error messages, intuitive CLI
4. **Extensibility** - Easy to add new languages and features

### Roadmap

- [ ] Add more language support (Dart, Elixir, Haskell, etc.)
- [ ] Web-based playground mode
- [ ] VS Code extension integration
- [ ] Docker container execution
- [ ] AI-powered code suggestions

---

## 📦 Build & Deployment

### Building from Source

```bash
# Clone repository
git clone https://github.com/gitstq/codesprint.git
cd codesprint

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Build package
python -m build
```

### Supported Environments

- **Operating Systems**: Linux, macOS, Windows
- **Python Versions**: 3.8, 3.9, 3.10, 3.11, 3.12

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read our [Contributing Guide](CONTRIBUTING.md) for details.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by SOLO Agent
</p>

---

<a name="简体中文"></a>
# 🚀 CodeSprint

<div align="center">

**轻量级多语言代码片段智能运行器 CLI**

*零依赖 • 自动语言检测 • 沙箱执行 • 精美TUI输出*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

</div>

---

## 🎉 项目介绍

**CodeSprint** 是一款轻量级、零依赖的命令行工具，让您可以直接在终端中**运行 18+ 种编程语言的代码片段**。无需在不同 IDE 之间切换，无需安装重型工具——只需编写并运行！

### 为什么选择 CodeSprint？

- ❌ **厌倦了** 为不同语言切换不同的 IDE？
- ❌ **苦恼于** 仅仅测试简单代码片段就要安装重型工具？
- ❌ **厌烦了** 复杂的代码游乐场设置流程？

**CodeSprint 解决所有这些问题！** ✅

### 🌟 核心特性

| 特性 | 描述 |
|------|------|
| 🔍 **自动语言检测** | 自动从文件扩展名、shebang 或代码模式检测语言 |
| 🚀 **18+ 种语言** | Python、JavaScript、TypeScript、Go、Rust、Java、C、C++、Ruby、PHP、Bash、Perl、Lua、R、Kotlin、Swift、Scala 等 |
| 🔒 **沙箱执行** | 安全隔离执行，带超时保护 |
| 📊 **精美 TUI 输出** | 彩色语法高亮输出，含执行统计 |
| 📚 **历史管理** | 追踪所有执行记录，标记收藏，搜索和导出 |
| 💻 **交互式 REPL 模式** | 在交互环境中快速测试代码 |
| 🔄 **批量执行** | 一次运行多个文件或代码片段 |
| ⚡ **零依赖** | 纯 Python 实现，无需外部依赖 |

---

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- 您想执行的语言运行时（如 JavaScript 需要 `node`，Go 需要 `go`）

### 安装

```bash
# 从 PyPI 安装
pip install codesprint

# 或从源码安装
git clone https://github.com/gitstq/codesprint.git
cd codesprint
pip install -e .
```

### 基本用法

```bash
# 运行文件
codesprint script.py

# 运行内联代码
codesprint -c "print('Hello, World!')"

# 显式指定语言
codesprint -l javascript -c "console.log('Hello!')"

# 交互模式
codesprint -i

# 列出可用运行时
codesprint -L
```

---

## 📖 详细使用指南

### 运行文件

```bash
# 运行 Python 文件
codesprint main.py

# 运行 JavaScript 文件
codesprint app.js

# 运行 Go 文件
codesprint main.go

# 设置自定义超时（秒）
codesprint --timeout 60 slow_script.py
```

### 内联代码执行

```bash
# Python
codesprint -c "import sys; print(sys.version)"

# JavaScript
codesprint -l js -c "console.log(process.version)"

# Ruby
codesprint -l ruby -c "puts RUBY_VERSION"
```

### 交互式 REPL 模式

```bash
codesprint -i
```

```
🚀 CodeSprint 交互模式
════════════════════════════════════════════════════════════════
输入代码并按回车执行。输入 'exit' 或 'quit' 退出。

>>> print('你好，世界！')

✅ 成功  PYTHON  ⏱ 0.012秒
──────────────────────────────────────────────────

📤 输出：
  你好，世界！
```

### 历史管理

```bash
# 显示历史
codesprint -H

# 显示统计
codesprint -s

# 清除历史
codesprint --clear-history
```

### JSON 输出（用于脚本）

```bash
codesprint --json -c "print('hello')"
```

```json
{
  "success": true,
  "output": "hello\n",
  "error": "",
  "exit_code": 0,
  "execution_time": 0.015,
  "language": "python"
}
```

---

## 💡 设计思路与迭代规划

### 设计理念

CodeSprint 基于以下原则构建：

1. **零依赖** - 无外部依赖意味着更快的安装和更少的冲突
2. **安全优先** - 沙箱执行带超时保护，防止代码失控
3. **开发者体验** - 精美输出、有用的错误信息、直观的 CLI
4. **可扩展性** - 易于添加新语言和功能

### 迭代规划

- [ ] 添加更多语言支持（Dart、Elixir、Haskell 等）
- [ ] Web 版游乐场模式
- [ ] VS Code 扩展集成
- [ ] Docker 容器执行
- [ ] AI 驱动的代码建议

---

## 📦 打包与部署

### 从源码构建

```bash
# 克隆仓库
git clone https://github.com/gitstq/codesprint.git
cd codesprint

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 构建包
python -m build
```

### 支持环境

- **操作系统**：Linux、macOS、Windows
- **Python 版本**：3.8、3.9、3.10、3.11、3.12

---

## 🤝 贡献指南

欢迎贡献！以下是开始方式：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 提交 Pull Request

请阅读我们的[贡献指南](CONTRIBUTING.md)了解详情。

---

## 📄 开源协议

本项目采用 MIT 协议开源 - 详情请查看 [LICENSE](LICENSE) 文件。

---

<p align="center">
  由 SOLO Agent 用 ❤️ 制作
</p>

---

<a name="繁體中文"></a>
# 🚀 CodeSprint

<div align="center">

**輕量級多語言程式碼片段智慧執行器 CLI**

*零依賴 • 自動語言偵測 • 沙箱執行 • 精美TUI輸出*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

</div>

---

## 🎉 專案介紹

**CodeSprint** 是一款輕量級、零依賴的命令列工具，讓您可以直接在終端機中**執行 18+ 種程式語言的程式碼片段**。無需在不同 IDE 之間切換，無需安裝重型工具——只需編寫並執行！

### 為什麼選擇 CodeSprint？

- ❌ **厭倦了** 為不同語言切換不同的 IDE？
- ❌ **苦惱於** 僅僅測試簡單程式碼片段就要安裝重型工具？
- ❌ **厭煩了** 複雜的程式碼遊樂場設定流程？

**CodeSprint 解決所有這些問題！** ✅

### 🌟 核心特性

| 特性 | 描述 |
|------|------|
| 🔍 **自動語言偵測** | 自動從副檔名、shebang 或程式碼模式偵測語言 |
| 🚀 **18+ 種語言** | Python、JavaScript、TypeScript、Go、Rust、Java、C、C++、Ruby、PHP、Bash、Perl、Lua、R、Kotlin、Swift、Scala 等 |
| 🔒 **沙箱執行** | 安全隔離執行，帶逾時保護 |
| 📊 **精美 TUI 輸出** | 彩色語法高亮輸出，含執行統計 |
| 📚 **歷史管理** | 追蹤所有執行記錄，標記收藏，搜尋和匯出 |
| 💻 **互動式 REPL 模式** | 在互動環境中快速測試程式碼 |
| 🔄 **批次執行** | 一次執行多個檔案或程式碼片段 |
| ⚡ **零依賴** | 純 Python 實作，無需外部依賴 |

---

## 🚀 快速開始

### 環境需求

- Python 3.8 或更高版本
- 您想執行的語言執行環境（如 JavaScript 需要 `node`，Go 需要 `go`）

### 安裝

```bash
# 從 PyPI 安裝
pip install codesprint

# 或從原始碼安裝
git clone https://github.com/gitstq/codesprint.git
cd codesprint
pip install -e .
```

### 基本用法

```bash
# 執行檔案
codesprint script.py

# 執行內聯程式碼
codesprint -c "print('Hello, World!')"

# 明確指定語言
codesprint -l javascript -c "console.log('Hello!')"

# 互動模式
codesprint -i

# 列出可用執行環境
codesprint -L
```

---

## 📖 詳細使用指南

### 執行檔案

```bash
# 執行 Python 檔案
codesprint main.py

# 執行 JavaScript 檔案
codesprint app.js

# 執行 Go 檔案
codesprint main.go

# 設定自訂逾時（秒）
codesprint --timeout 60 slow_script.py
```

### 內聯程式碼執行

```bash
# Python
codesprint -c "import sys; print(sys.version)"

# JavaScript
codesprint -l js -c "console.log(process.version)"

# Ruby
codesprint -l ruby -c "puts RUBY_VERSION"
```

### 互動式 REPL 模式

```bash
codesprint -i
```

```
🚀 CodeSprint 互動模式
════════════════════════════════════════════════════════════════
輸入程式碼並按 Enter 執行。輸入 'exit' 或 'quit' 離開。

>>> print('你好，世界！')

✅ 成功  PYTHON  ⏱ 0.012秒
──────────────────────────────────────────────────

📤 輸出：
  你好，世界！
```

### 歷史管理

```bash
# 顯示歷史
codesprint -H

# 顯示統計
codesprint -s

# 清除歷史
codesprint --clear-history
```

### JSON 輸出（用於腳本）

```bash
codesprint --json -c "print('hello')"
```

```json
{
  "success": true,
  "output": "hello\n",
  "error": "",
  "exit_code": 0,
  "execution_time": 0.015,
  "language": "python"
}
```

---

## 💡 設計思路與迭代規劃

### 設計理念

CodeSprint 基於以下原則建構：

1. **零依賴** - 無外部依賴意味著更快的安裝和更少的衝突
2. **安全優先** - 沙箱執行帶逾時保護，防止程式碼失控
3. **開發者體驗** - 精美輸出、有用的錯誤訊息、直觀的 CLI
4. **可擴展性** - 易於新增新語言和功能

### 迭代規劃

- [ ] 新增更多語言支援（Dart、Elixir、Haskell 等）
- [ ] Web 版遊樂場模式
- [ ] VS Code 擴充功能整合
- [ ] Docker 容器執行
- [ ] AI 驅動的程式碼建議

---

## 📦 打包與部署

### 從原始碼建構

```bash
# 複製儲存庫
git clone https://github.com/gitstq/codesprint.git
cd codesprint

# 安裝開發依賴
pip install -e ".[dev]"

# 執行測試
pytest

# 建構套件
python -m build
```

### 支援環境

- **作業系統**：Linux、macOS、Windows
- **Python 版本**：3.8、3.9、3.10、3.11、3.12

---

## 🤝 貢獻指南

歡迎貢獻！以下是開始方式：

1. Fork 本儲存庫
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 提出 Pull Request

請閱讀我們的[貢獻指南](CONTRIBUTING.md)了解詳情。

---

## 📄 開源授權

本專案採用 MIT 授權條款開源 - 詳情請查看 [LICENSE](LICENSE) 檔案。

---

<p align="center">
  由 SOLO Agent 用 ❤️ 製作
</p>
