# 🚀 Codex CLI 中文汉化工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows/)

一个专为 Codex CLI 0.40.0 版本设计的中文汉化工具，提供简洁易用的图形化界面。

## ✨ 功能特点

- 🔍 **智能检测** - 自动检测 Node.js 和 Codex CLI 安装状态
- 🔄 **版本管理** - 自动检测最新版本并提供更新提示  
- 🌍 **一键汉化** - 将 Codex CLI 界面完全汉化为中文
- 🔄 **快速恢复** - 可随时恢复英文原版界面
- ⚡ **专业优化** - 专为 Codex CLI 0.40.0 版本优化
- 🎯 **界面简洁** - 现代化暗黑主题，操作简便

## 📋 系统要求

- **操作系统**: Windows 10/11
- **Node.js**: 已安装 ([下载地址](https://nodejs.org/zh-cn/download/))
- **Codex CLI**: 0.40.0 版本 (`npm install -g @openai/codex`)

## 🚀 快速开始

### 方式一：直接下载可执行文件（推荐）

1. 从 [Releases](https://github.com/396001000/codex-Chinese/releases) 下载最新版本的 `Codex CLI汉化工具.exe`
2. 双击运行程序
3. 点击 "检测安装" 确认 Codex CLI 状态
4. 点击 "一键汉化" 开始汉化

### 方式二：从源码运行

1. **克隆仓库**
   ```bash
   git clone https://github.com/396001000/codex-Chinese.git
   cd codex-Chinese
   ```

2. **安装依赖**
   ```bash
   cd codex-gui-simple
   pip install -r requirements.txt
   ```

3. **运行程序**
   ```bash
   python codex_gui.py
   ```

## 📖 使用指南

### 1. 检测环境
- 启动程序后，首先点击 **"检测安装"** 按钮
- 程序会自动检测 Node.js 和 Codex CLI 的安装状态
- 确保显示 ✅ Codex CLI: v0.40.0

### 2. 执行汉化
- 确认版本正确后，点击 **"一键汉化"** 按钮
- 等待汉化完成，通常需要几秒钟
- 看到成功提示后，Codex CLI 已完全中文化

### 3. 恢复原版
- 如需恢复英文界面，点击 **"恢复原版"** 按钮
- 确认操作后，界面将恢复为英文原版

## 🎯 支持版本

本工具专为 **Codex CLI 0.40.0** 版本设计，确保最佳兼容性和稳定性。

## 📁 项目结构

```
codex-Chinese/
├── inject-chinese-final-dedup.js    # 核心汉化脚本
├── codex-translations-extended.json # 扩展翻译文件
├── codex-gui-simple/                # 图形化工具
│   ├── codex_gui.py                 # 主程序
│   ├── requirements.txt             # 依赖列表
│   ├── app_icon.ico                 # 程序图标
│   └── README.md                    # 详细说明
└── README.md                        # 项目说明
```

## 🛠️ 开发者信息

### 技术栈
- **界面框架**: CustomTkinter (现代化暗黑主题)
- **汉化引擎**: Node.js + 自定义注入脚本
- **打包工具**: Nuitka (原生C++编译)

### 汉化原理
1. 通过 Node.js 执行汉化脚本
2. 动态替换 Codex CLI 界面文本
3. 保留原版备份，支持随时恢复

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## ⚠️ 注意事项

- 本工具仅支持 Codex CLI 0.40.0 版本
- 汉化前请确保 Codex CLI 正常工作
- 建议在汉化前备份重要配置
- 如遇问题，可先尝试恢复原版

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE) 开源。

## 📞 联系方式

- **作者微信**: chaojigeti520
- **项目地址**: https://github.com/396001000/codex-Chinese
- **支持定制**: 软件开发定制服务

---

**⭐ 如果这个项目对您有帮助，请给个 Star 支持一下！**

## 🔄 更新日志

### v1.0.0 (2025-09-25)
- 🎉 首次发布
- ✅ 支持 Codex CLI 0.40.0 汉化
- ✅ 图形化界面
- ✅ 一键汉化/恢复功能
- ✅ 智能环境检测