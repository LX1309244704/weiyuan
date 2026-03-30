# 微元 Weiyuan - 全生态RPA自动化平台

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/RPA-Automation-green.svg" alt="RPA">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20|%20macOS%20|%20Linux-lightgrey.svg" alt="Platform">
</p>

<p align="center">
  <b>一站式全生态RPA自动化平台</b><br>
  低代码 · 全生态 · AI增强 · 开箱即用
</p>

---

## 🚀 项目简介

**微元（Weiyuan）**是一个功能强大的全生态RPA（机器人流程自动化）平台，让你通过简单的YAML配置，就能实现跨平台的自动化操作。无需编程基础，复制模板即可使用。

### ✨ 为什么选择微元？

| 特性 | 传统RPA工具 | 微元 |
|------|------------|------|
| 学习成本 | 需要编程基础 | 🟢 YAML配置，零代码 |
| 生态覆盖 | 单一平台 | 🟢 飞书+微信+抖音+小红书 |
| AI能力 | 无 | 🟢 内置OCR+大模型 |
| 使用方式 | 命令行 | 🟢 CLI+PC客户端+Web控制台 |
| 价格 | 付费订阅 | 🟢 完全免费开源 |

---

## 🎯 核心能力

### 1️⃣ RPA流程引擎
- ✅ **低代码流程定义**：YAML格式，5分钟上手
- ✅ **多维度触发**：定时、Webhook、事件、手动、条件触发
- ✅ **可视化执行**：实时日志、步骤追踪、错误重试
- ✅ **数据传递**：步骤间上下文自动传递，支持变量和表达式

### 2️⃣ 全生态插件（已内置10+）

#### 💼 飞书生态
| 插件 | 功能 |
|------|------|
| `feishu/bitable` | 多维表格：增删改查、批量导入导出 |
| `feishu/message` | 消息：文本/图片/卡片发送 |
| `feishu/doc` | 文档：创建、读取、更新、导出 |

#### 💬 微信全生态
| 插件 | 功能 |
|------|------|
| `wechat/message` | 个人微信：给好友/群发消息、文件、图片 |
| `wechat/work` | 企业微信：内部消息、客户联系、外部客户群发 |
| `wechat/mp` | 公众号：模板消息、客服消息、粉丝管理 |

#### 📱 内容平台
| 插件 | 功能 |
|------|------|
| `publish/content` | 小红书/抖音/视频号：一键发布图文/视频 |

#### 🖥️ UI自动化
| 插件 | 功能 |
|------|------|
| `ui/desktop` | 桌面自动化：鼠标/键盘、截图、图像识别 |
| `ui/browser` | 浏览器自动化：网页操作、元素定位、表单填写 |

#### 🤖 AI增强
| 插件 | 功能 |
|------|------|
| `ai/ocr` | OCR识别：图片/截图文字提取，支持中英文 |
| `ai/llm` | 大模型：GPT/Claude/通义千问，文本生成、摘要、翻译 |

#### 🛠️ 基础工具
| 插件 | 功能 |
|------|------|
| `data/process` | 数据处理：过滤、排序、聚合、Excel/CSV处理 |
| `file/operation` | 文件操作：读写、复制、移动、批量处理 |
| `http/request` | HTTP请求：调用API、数据同步 |

### 3️⃣ 多端使用方式

#### 🖥️ PC客户端（推荐）
```bash
python start_gui.py
```
可视化界面，点按钮就能操作，适合非技术人员。

#### 🌐 Web控制台
```bash
opencli rpa web
# 打开 http://localhost:8888
```
浏览器访问，支持手机端，适合团队协作。

#### ⌨️ CLI命令行
```bash
opencli rpa run my_flow.yaml
```
适合技术人员批量执行和自动化调度。

---

## 📦 快速开始

### 1. 安装

```bash
# 克隆项目
git clone https://github.com/LX1309244704/weiyuan.git
cd weiyuan

# 安装依赖（全量安装）
pip install -r requirements.txt
pip install -r requirements_rpa.txt
pip install -r requirements_gui.txt
```

### 2. 第一个RPA流程

创建 `hello.yaml`：
```yaml
name: 我的第一个RPA流程
steps:
  - name: 发送消息到企业微信
    uses: wechat/work@1.0.0
    with:
      action: send_text
      corp_id: "你的企业ID"
      corp_secret: "你的Secret"
      agent_id: 1000001
      receiver: "@all"
      content: "🎉 我的第一个RPA流程运行成功！"
```

执行：
```bash
opencli rpa run hello.yaml
```

### 3. 使用内置模板

```bash
# 查看所有模板
opencli rpa list

# 使用模板创建流程
opencli rpa init 库存预警 -t inventory_alert
opencli rpa init 每日报表 -t daily_sales_report
opencli rpa init 微信发消息 -t wechat_send_message
opencli rpa init 多平台发布 -t multi_platform_publish
```

---

## 💡 典型使用场景

### 场景1：企业微信客户自动维护
```yaml
# 每天9点自动给新客户发欢迎消息
trigger:
  type: schedule
  cron: "0 9 * * *"

steps:
  - name: 获取昨日新增客户
    uses: wechat/work@1.0.0
    with:
      action: get_external_contact_list
    register: new_customers
  
  - name: 批量发送欢迎消息
    uses: wechat/work@1.0.0
    with:
      action: batch_send_external_message
      external_userids: "${{ steps.获取昨日新增客户.output.external_userids }}"
      content: "您好！欢迎添加我们，有任何问题随时找我~"
```

### 场景2：飞书多维表格数据自动同步到微信群
```yaml
steps:
  - name: 导出今日销售数据
    uses: feishu/bitable@1.0.0
    with:
      action: export_excel
      app_token: "xxx"
      table_id: "xxx"
      output_path: "./今日销售.xlsx"
  
  - name: 发送到微信群
    uses: wechat/message@1.0.0
    with:
      receiver: "业务群"
      msg_type: file
      file_path: "./今日销售.xlsx"
      at_all: true
```

### 场景3：小红书/抖音/视频号内容一键发布
```yaml
steps:
  - name: 发布小红书
    uses: publish/content@1.0.0
    with:
      platform: xiaohongshu
      title: "打工人必备神器！RPA自动化工具"
      content: "每天重复工作太枯燥？试试这个工具..."
      files: ["./封面.png", "./内容1.png"]
      tags: ["RPA", "效率工具"]
  
  - name: 发布抖音
    uses: publish/content@1.0.0
    with:
      platform: douyin
      title: "3分钟学会RPA"
      content: "教程视频来了..."
      files: ["./教程.mp4"]
```

### 场景4：自动截图识别文字并保存
```yaml
steps:
  - name: 截图
    uses: ui/desktop@1.0.0
    with:
      action: screenshot
      save_path: "./screenshot.png"
  
  - name: OCR识别
    uses: ai/ocr@1.0.0
    with:
      action: recognize
      image_path: "./screenshot.png"
    register: ocr_result
  
  - name: 保存到飞书
    uses: feishu/bitable@1.0.0
    with:
      action: create_record
      app_token: "xxx"
      table_id: "xxx"
      fields:
        "内容": "${{ steps.OCR识别.output.full_text }}"
```

---

## 📁 项目结构

```
weiyuan/
├── 📄 README.md                 # 项目说明
├── 📦 requirements.txt          # 依赖文件
├── 🚀 start_gui.py             # 启动PC客户端
├── 🐳 Dockerfile               # Docker部署
│
├── rpa/                        # RPA核心代码
│   ├── core/                   # 核心引擎
│   │   ├── engine.py          # 执行引擎
│   │   ├── flow.py            # 流程解析
│   │   ├── plugin.py          # 插件系统
│   │   └── variable_engine.py # 变量引擎
│   ├── plugins/               # 插件集合
│   │   ├── feishu_plugins.py  # 飞书插件
│   │   ├── wechat_plugins.py  # 微信全生态
│   │   ├── ui_plugins.py      # UI自动化
│   │   ├── ocr_plugin.py      # OCR识别
│   │   ├── ai_plugin.py       # AI大模型
│   │   └── publish_plugins.py # 内容发布
│   ├── templates/             # 流程模板
│   ├── cli/                   # 命令行工具
│   ├── gui/                   # PC客户端
│   └── web/                   # Web控制台
│
├── feishu_core/               # 飞书核心功能（底层API）
├── ai_integration/            # AI集成模块
├── workflows/                 # 工作流引擎
├── visualization/            # 数据可视化
└── flows/                    # 用户流程存放目录
```

---

## 📖 完整文档

| 文档 | 说明 |
|------|------|
| [README_RPA.md](README_RPA.md) | RPA工具完整使用指南 |
| [README_GUI.md](README_GUI.md) | PC客户端使用指南 |
| [README_DEPLOY.md](README_DEPLOY.md) | 部署指南（Docker/Railway等） |

---

## 🛣️ 开发路线图

### ✅ v1.0.0 已完成
- [x] RPA核心引擎
- [x] 飞书生态插件
- [x] 微信个人插件
- [x] PC客户端

### ✅ v2.0.0 已完成
- [x] 企业微信插件
- [x] 公众号插件
- [x] UI自动化插件
- [x] OCR插件
- [x] AI大模型插件
- [x] Web控制台
- [x] 内容发布插件（小红书/抖音/视频号）

### 📅 v3.0.0 计划中
- [ ] 更多内容平台（B站/知乎/微博）
- [ ] 数据库插件（MySQL/PostgreSQL/MongoDB）
- [ ] 邮件插件（SMTP/IMAP）
- [ ] 定时任务调度优化
- [ ] 云端托管版本

---

## 🤝 贡献指南

欢迎贡献代码！无论是：
- 🐛 修复Bug
- ✨ 新增插件
- 📖 完善文档
- 💡 提出建议

请参考 [贡献指南](CONTRIBUTING.md)。

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 👥 关于作者

- **作者**：三金的小虾米
- **邮箱**：1309244704@qq.com
- **GitHub**：https://github.com/LX1309244704
- **项目主页**：https://github.com/LX1309244704/weiyuan

---

<p align="center">
  <b>🦞 微元 Weiyuan - 让自动化触手可及！</b>
</p>
