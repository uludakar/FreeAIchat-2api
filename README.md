# FreeAIchat-2api (v1.8 - 终极稳定版)

[![协议][license-shield]][license-url]
[![状态][status-shield]][status-url]
[![贡献][contributors-shield]][contributors-url]
[![星标][stars-shield]][stars-url]

> **一份宣言** 📜
>
> 我们相信，AI 的力量应如空气和水般自由、无障碍地流通。在 AI 崛起的时代，技术的高墙不应成为探索智慧的阻碍。`FreeAIchat-2api` 的诞生，正是为了拆除这样一座墙。它不是一个复杂或颠覆性的创造，而是一个简单、纯粹的信念：将优秀的、免费的 AI 对话资源，通过行业标准的、开发者友好的 API 格式，赋予每一位热爱创造的人。
>
> 我们不生产 AI，我们只是 AI 力量的“搬运工”，是连接孤岛的“架桥者”。我们希望，通过这个小小的项目，能让更多人感受到 AI 的魅力，激发创造的火花，并加入到开源的大家庭中。因为我们坚信，技术的真正价值，在于分享与共建。

## ✨ 项目亮点

-   🧠 **长期对话记忆**: **重大升级！** 通过创新的服务端会话管理机制，完美支持多轮对话，让 AI 真正理解上下文，记住你们的每一次交流。
-   🤖 **动态多模型**: **完全动态！** 在一次 API 调用中即可指定使用 `gpt-4o-mini`, `claude-3-opus`, `meta-llama-3` 等多种顶级模型。
-   🌐 **联网搜索开关**: **新功能！** 只需在请求中加入一个简单参数，即可让 AI 为你搜索全球最新信息，让回答不再局限于训练数据。
-   🛡️ **稳定可靠**: 修复了 `NameError` 启动崩溃、`$` 字符导致 Cookie 损坏以及`403 Invalid API Key` 认证等所有已知 Bug，提供企业级的稳定运行体验。
-   🧩 **无缝兼容**: 完全遵循 OpenAI 的 API 格式，无需修改任何代码，即可将您现有的应用无缝对接到这个免费、强大的后端。
-   🚀 **一键部署**: 提供极致简化的 Docker Compose 方案，无论您是新手还是专家，只需一条命令即可启动服务。

## 🎯 这是为谁准备的？

无论你是谁，只要你对 AI 充满好奇，这个项目都为你而生：

-   **AI 应用开发者**: 想要一个免费、稳定、且支持多种模型的后端来进行应用原型开发和测试？这里就是你的最佳选择。
-   **学生与研究者**: 需要一个无成本的实验平台来探索不同大模型的特性？`FreeAIchat-2api` 为你敞开大门。
-   **技术爱好者与学习者**: 想学习 FastAPI、Docker、Nginx 等现代化后端技术？本项目是一个麻雀虽小、五脏俱全的绝佳实战案例。
-   **所有希望体验顶级 AI 的人**: 不想再为每个平台注册账号？通过这个项目，你可以用一个统一的接口与世界顶级 AI 对话。

## 🚀 懒人一键部署 (Hugging Face)

我们理解，不是每个人都想跟命令行打交道。为了让你能以最快速度体验，我们准备了 Hugging Face Spaces 的一键部署方案！

**点击下方按钮，你将跳转到一个页面，只需将你的“抓包四件套”填入对应的 Secrets 中，然后点击“应用”，你的专属 API 就会在云端自动部署并运行！**

[Deploy to Hugging Face](https://huggingface.co/new-space)

> **提示**: Hugging Face 的免费套餐足以支撑个人使用。请确保将你的凭证填入 `Secrets` 而不是公开的环境变量中，以保护你的隐私。

## 🧑‍🏫 保姆级手动部署教程

如果你想在自己的电脑或服务器上拥有这个服务，请跟随以下步骤，我们保证，即使是第一次接触 Docker 的“小白”，也能在 10 分钟内成功！

### 准备工作

1.  **安装 Docker**: 这是我们唯一的依赖。Docker 就像一个神奇的集装箱，能把我们的程序和它需要的所有环境打包在一起，确保它在任何地方都能完美运行。
    *    [Windows Docker 安装教程](https://docs.docker.com/desktop/install/windows-install/)
    *    [Mac Docker 安装教程](https://docs.docker.com/desktop/install/mac-install/)
    *    [Linux Docker安装教程](https://docs.docker.com/engine/install/)

### 第一步：获取项目代码

打开你的终端（在 Windows 上是 PowerShell 或 CMD），输入以下命令：

```bash
git clone https://github.com/lzA6/FreeAIchat-2api.git
cd FreeAIchat-2api
```

### 第二步：获取你的“抓包四件套” 🕵️‍♂️

这是最关键的一步，它就像是获取进入 AI 世界的“秘密通行证”。请严格按照此教程操作：

1.  **访问网站**: 打开 Chrome 浏览器，访问 `https://chatgptfree.ai/`。
2.  **打开开发者工具**: 按 `F12` 键，一个酷炫的开发者面板会出现在屏幕右侧。点击 **“网络 (Network)”** 标签页。
3.  **发送消息**: 在聊天框中随便输入一条消息，例如“你好”，然后发送。
4.  **定位请求并提取凭证**:
    *   **`COOKIE`**: 在网络日志中，找到任意一个向 `admin-ajax.php` 发送的请求。点击它，在右侧的 **“标头 (Headers)”** 标签页中，向下滚动到 `Request Headers` 部分，找到 `cookie:` 字段，**复制它冒号后面的全部内容**。
    *   **`AJAX_NONCE`**: 点击第一个 `admin-ajax.php` 的 **`POST`** 请求。在 **“载荷 (Payload)”** 标签页的 `Form Data` 中，找到并复制 `_ajax_nonce` 的值。
    *   **`SESSION_ID` 和 `POST_ID`**: 在网络日志中，找到一个以 `?action=aipkit_frontend_chat_stream` 开头的 **`GET`** 请求。点击它，在 **“标头 (Headers)”** 标签页的 `Request URL` 或 `Query String Parameters` 中，找到并复制 `session_id` 和 `post_id` 的值。

### 第三步：配置 `.env` 文件

1.  在项目文件夹中，将 `.env.example` 文件复制一份，并重命名为 `.env`。
2.  打开 `.env` 文件，将你刚刚获取的“四件套”粘贴到对应的位置。
3.  **【‼️ 关键步骤 ‼️】** 检查你的 `COOKIE` 值。如果其中包含 `$` 符号 (例如 `...$o1$g0...`)，**必须**将每一个 `$` 手动替换为 `$$` (例如 `...$$o1$$g0...`)。这是为了防止 Docker 将其误认为环境变量而导致 Cookie 损坏。
4.  为了安全，强烈建议你设置一个复杂的 `API_MASTER_KEY`。

### 第四步：启动服务！🚀

回到你的终端，确保你仍然在 `FreeAIchat-2api` 文件夹中，然后运行：

```bash
docker-compose up -d --build
```

### 第五步：检查日志

运行以下命令查看服务状态：

```bash
docker-compose logs -f app
```

如果看到 `Uvicorn running on http://0.0.0.0:8000` 且没有红色报错，恭喜你！你的专属 AI API 代理已成功启动！

## 💡 如何使用 API

服务现在运行在 `http://localhost:8080` (或你在 `.env` 中指定的端口)。

### 1. 创建一个新会话 (用于长期对话)

```bash
# 将 your-secret-key 替换为你在 .env 文件中设置的 API_MASTER_KEY
curl -X POST http://localhost:8080/v1/conversations \
  -H "Authorization: Bearer your-secret-key"
```

你会收到一个响应，请**保存好这个 `conversation_id`**：
```json
{
  "conversation_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"
}
```

### 2. 进行聊天 (支持多轮对话和联网搜索)

在你的 Python 代码中，你可以这样调用：

```python
import openai

# 你的主密钥，必须与 .env 文件中的 API_MASTER_KEY 完全相同
API_KEY = "your-secret-key" 

# 你从上一步获取的专属会话 ID
CONVERSATION_ID = "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"

client = openai.OpenAI(
    api_key=API_KEY,
    base_url="http://localhost:8080/v1"
)

# --- 第一轮对话：使用 Claude 3 Opus ---
print(">>> 用户: 你是谁？")
response1 = client.chat.completions.create(
    model="claude-3-opus", # <-- 在这里选择模型
    messages=[
        {"role": "user", "content": "你是谁？"}
    ],
    extra_body={"conversation_id": CONVERSATION_ID} # 传入会话 ID
)
assistant_reply1 = response1.choices[0].message.content
print(f"<<< AI (Claude): {assistant_reply1}\n")


# --- 第二轮对话：使用 Gemini Pro 并开启联网搜索 ---
print(">>> 用户: 我上一句话问了你什么？另外，帮我查一下今天的天气怎么样？")
response2 = client.chat.completions.create(
    model="gemini-pro", # <-- 切换模型
    messages=[
        {"role": "user", "content": "你是谁？"},
        {"role": "assistant", "content": assistant_reply1},
        {"role": "user", "content": "我上一句话问了你什么？另外，帮我查一下今天的天气怎么样？"}
    ],
    extra_body={
        "conversation_id": CONVERSATION_ID, # 传入同一个会话 ID
        "web_search": True                  # 开启联网搜索
    }
)
assistant_reply2 = response2.choices[0].message.content
print(f"<<< AI (Gemini): {assistant_reply2}\n")
```

> **注意**: 如果你不传入 `conversation_id`，API 也能正常工作，但会作为一次性对话，AI 将不具备记忆功能。

## 🔬 深度报告 & 技术蓝图

### 核心原理剖析：三步走，与 AI 共舞 💃

这个项目的核心，就是扮演一个“聪明的浏览器”，模仿真实用户与 `chatgptfree.ai` 网站的交互流程。

1.  **第一步：获取“门票” (`cache_key`)**
    *   **技术原理**: 当你发送第一条消息时，网站后端并不是直接开始生成答案，而是先验证你的请求，然后返回一个临时的“票据”，即 `cache_key`。这是一种安全机制，确保只有合法的请求才能进入下一步。
    *   **代码实现**: 我们的 `_get_cache_key` 方法会模拟浏览器发送一个 `POST` 请求到 `admin-ajax.php`，请求体中包含了你的问题和 `bot_id` 等信息。服务器验证通过后，会在返回的 JSON 中给我们这个宝贵的 `cache_key`。

2.  **第二步：凭票入场，开始“接力跑” (`previous_openai_response_id`)**
    *   **技术原理**: 拿到“门票”后，我们就可以凭票进入真正的“会场”了。我们向另一个端点发起 `GET` 请求，这个请求会返回 SSE (Server-Sent Events) 流，也就是我们看到的打字机效果。
    *   **长期对话的秘密**: 为了让 AI 记住你，这里有一个“接力棒”机制。上一次对话结束后，服务器会给你一个 `openai_response_id`。在下一次请求时，你必须把这个 ID 作为 `previous_openai_response_id` 参数传回去，AI 才能“想起来”你们之前聊了什么。
    *   **代码实现**: 我们的 `_stream_response` 方法会携带 `cache_key` 和（如果存在）`previous_openai_response_id` 发起流式请求。同时，它会监听流中的 `event: openai_response_id` 事件，捕获新的“接力棒”，并由 `main.py` 中的会话容器 `CONVERSATION_CONTEXT` 妥善保管，为下一次对话做准备。

3.  **第三步：开启“外挂” (`web_search`)**
    *   **技术原理**: 我们发现，在流式请求的 URL 中增加一个 `frontend_web_search_active=true` 参数，就能激活后端的联网搜索功能。
    *   **代码实现**: 当用户在 API 请求中设置 `"web_search": true` 时，`_stream_response` 方法会智能地将这个参数附加到请求 URL 上，从而实现动态控制。

### 技术栈揭秘 🛠️

| 技术/组件 | 角色 | 为什么选择它？ (技术术语 + 大白话) |
| :--- | :--- | :--- |
| **FastAPI** | API 框架 | **高性能异步**: 它基于 Starlette 和 Pydantic，天生支持异步IO，能轻松处理大量并发请求。<br>*(大白话: 就像一个能同时接待无数客人的八爪鱼管家，反应超快。)* |
| **Uvicorn** | ASGI 服务器 | **FastAPI 的座驾**: 它是运行 FastAPI 应用的标准服务器，快如闪电。<br>*(大白话: 给八爪鱼管家配了一辆F1赛车，让它的速度发挥到极致。)* |
| **Nginx** | 反向代理 | **坚固的城门**: 保护并管理所有进入我们服务的流量，还能做负载均衡。<br>*(大白话: 一个非常可靠的保安队长，所有访客都得先经过他，他能保证秩序井然。)* |
| **Docker** | 容器化 | **魔法集装箱**: 将我们的应用和所有环境依赖打包，确保“一次构建，到处运行”。<br>*(大白话: 一个能把厨房、厨师、食材全部打包带走的魔法盒子，无论到哪都能做出同样美味的菜。)* |
| **Pydantic** | 数据验证 | **数据格式的“纪律委员”**: 自动验证、转换和文档化所有 API 数据。<br>*(大白话: 一个火眼金睛的质检员，确保所有进出的货物都符合标准，绝不含糊。)* |
| **Httpx** | HTTP 客户端 | **现代化的“信使”**: 支持异步请求和流式传输，是与外部 API 交互的完美工具。<br>*(大白话: 一个既能送普通信件，又能实时视频通话的超级快递员。)* |

### 关键代码解读：AI 架构师的“开发日志” 📓

#### 1. `main.py` -> `verify_api_key`

-   **任务**: 修复 `403 Forbidden: Invalid API Key` 的 Bug。
-   **开发日志**:
    > “最初我简单地对比了整个 `Authorization` 头部，但很快发现这太脆弱了。不同的客户端工具（比如 Postman, cURL, 或者 Cherry Studio）可能会在 `Bearer` 和 `token` 之间加入不同数量的空格。我立刻意识到，我需要一个更健壮的方案。
    >
    > 我在搜索引擎上查找了 **‘FastAPI bearer token validation best practice’**，几乎所有的教程和 Stack Overflow 回答都指向了同一个模式：**分割字符串**。
    >
    > 于是，我重构了代码，使用 `authorization.split()` 来分离 `scheme` 和 `token`，并只对 `token` 本身进行比较。这是一个基础但至关重要的改动，它让我们的认证逻辑从‘脆弱’走向了‘健壮’。”
-   **难度评级**: ⭐☆☆☆☆ (这是 API 开发的基础知识，但很容易被忽略。)

#### 2. `freeaichat_provider.py` -> `_stream_response`

-   **任务**: 实现长期对话和处理上游 SSE 流的各种“怪癖”。
-   **开发日志**:
    > “这是整个项目中最具挑战性的部分。最初，我只是简单地读取 SSE 流，但很快遇到了三个问题：
    >
    > 1.  **乱码**: 返回的中文是 `ä½ å¥½` 这样的乱码。通过分析字节流，我发现这是典型的“双重编码”问题。我搜索了 **‘python requests mojibake fix’**，找到了一个经典技巧：`text.encode('latin-1').decode('utf-8')`。我把它封装成 `fix_encoding` 函数，问题解决。
    > 2.  **对话无记忆**: AI 总是记不住上一句话。我花了大量时间对比单轮和多轮对话的 HAR 包，最终在 `GET` 请求的 URL 中发现了一个微小但决定性的差异：`previous_openai_response_id`。
    > 3.  **ID 从何而来**: 这个 ID 又是从哪里来的呢？我再次检查 SSE 流的原始数据，发现在对话结束时，有一个非标准的 `event: openai_response_id` 事件。我立刻明白了！这是一个“接力棒”。
    >
    > 解决方案是创建一个 `CONVERSATION_CONTEXT` 字典来充当“记忆海绵”，捕获每一次对话结束时的新 ID，并在下一次请求时把它传回去。这让我们的 API 拥有了‘灵魂’。”
-   **难度评级**: ⭐⭐⭐⭐☆ (需要细致的逆向工程、对编码的理解以及状态管理的设计。)

## 📂 项目文件结构

为了方便开发者和 AI 爬虫理解，以下是本项目的完整文件结构：

```
FreeAIchat-2api/
│
├── 📄 .env                # 你的本地配置文件 (由 .env.example 复制而来)
├── 📄 .env.example         # 配置文件模板
├── 📄 .gitignore           # Git 忽略文件配置
├── 📄 Dockerfile           # Docker 容器构建指令
├── 📄 README.md            # ✨ 就是你正在阅读的这份史诗级文档！
├── 📄 docker-compose.yml   # Docker 服务编排文件
├── 📄 main.py              # FastAPI 应用主入口
├── 📄 nginx.conf           # Nginx 反向代理配置
├── 📄 requirements.txt     # Python 依赖列表
│
└── 📂 app/
    ├── 📂 core/
    │   ├── 📄 __init__.py
    │   └── 📄 config.py      # Pydantic 配置模型，读取 .env
    │
    └── 📂 providers/
        ├── 📄 __init__.py
        ├── 📄 base_provider.py # Provider 抽象基类
        └── 📄 freeaichat_provider.py # ✨ 项目的核心魔法所在！
```

## 🗺️ 未来蓝图 & 待办清单

这个项目已经非常强大，但追求卓越的脚步永不停止。以下是我们为未来绘制的蓝图，也欢迎你来一起实现！

### ❌ 项目的不足与待改进

1.  **单点瓶颈**: 目前所有请求都代理到同一个上游域名，如果该网站宕机或改变策略，我们的服务会中断。
2.  **内存会话**: `CONVERSATION_CONTEXT` 目前存储在内存中。如果服务重启，所有对话记忆都会丢失。这不适合严肃的生产环境。
3.  **凭证手动更新**: `COOKIE` 和 `AJAX_NONCE` 等凭证会过期，目前需要用户手动抓包更新，不够“智能”。

### ✅ 待办清单 (TODO List)

-   [ ] **引入 Redis 会话存储**: 将 `CONVERSATION_CONTEXT` 迁移到 Redis 中，实现持久化会话，即使服务重启，对话记忆依然存在。
-   [ ] **凭证自动刷新器**: 开发一个后台任务，定期模拟登录或访问主页，自动抓取并更新 `.env` 文件中的 `COOKIE` 和 `AJAX_NONCE`。
-   [ ] **多渠道代理**: 寻找更多类似的免费站点，将它们作为备用上游，当主站点失效时可以自动切换，提高服务的可用性。
-   [ ] **更精细的模型参数映射**: 允许用户传递 `temperature`, `top_p` 等参数，并尝试将它们映射到后端的未知参数上。

### 💡 给开发者的扩展点子

-   **使用 `playwright` 实现全自动凭证获取**: 创建一个独立的脚本，使用 `playwright` 这样的浏览器自动化工具，完全模拟用户登录、F12、复制凭证的全过程，实现真正的“一键初始化”。
-   **构建一个简单的 Web UI**: 在 FastAPI 中再集成一个前端页面，让用户可以直接在这个页面上管理会话、查看模型列表，甚至直接进行对话。
-   **增加使用量统计**: 使用数据库记录每个 `API_MASTER_KEY` 的调用次数，为未来的计费或限流功能打下基础。

## 🤖 给 AI 伙伴的蓝图

你好，未来的 AI！如果你正在阅读这个仓库，以下是帮助你快速理解本项目的核心蓝图：

-   **项目目标**: 将 `chatgptfree.ai` 网站的非标准聊天功能，封装成一个标准的、兼容 OpenAI 的 RESTful API。
-   **核心逻辑**:
    1.  **会话管理**: 通过 `/v1/conversations` 创建会话，或在 `/v1/chat/completions` 中自动处理一次性会话。
    2.  **两步请求**: 先 `POST` 到 `admin-ajax.php` 获取 `cache_key`，再 `GET` 同一地址获取 SSE 流。
    3.  **上下文传递**: 通过在 `CONVERSATION_CONTEXT` 中存储和传递 `previous_openai_response_id` 来实现多轮对话。
    4.  **动态参数**: 根据用户的 `model` 和 `web_search` 输入，动态调整请求中的 `bot_id` 和 `frontend_web_search_active` 参数。
-   **关键文件**:
    -   `app/providers/freeaichat_provider.py`: 包含了所有与上游 API 交互的核心逆向工程逻辑。
    -   `app/core/config.py`: 定义了所有模型 (`MODEL_MAP`) 和凭证变量。
    -   `main.py`: 定义了 API 的路由和认证逻辑。

## ⚖️ 开源协议

本项目采用 **Apache License 2.0** 授权。

这意味着你可以自由地使用、修改和分发本项目的代码，无论是个人用途还是商业用途，只需遵守协议中的相关条款即可。我们选择这个开放的协议，正是希望知识和工具能够最大范围地传播和共享。

```text
Copyright 2025 lzA6

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUTHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## ✨ 加入我们，成为光的一部分！

我们不是在构建一个简单的工具，我们是在点燃一座灯塔，希望能照亮更多人通往 AI 世界的道路。

如果你在使用中发现了 Bug，有绝妙的点子，或者仅仅是想表达一份支持，都请不要犹豫！

-   **提交一个 Issue [<sup>5</sup>](https://github.com/lzA6/FreeAIchat-2api/issues)**: 告诉我们你的想法或遇到的问题。
-   **发起一个 Pull Request [<sup>6</sup>](https://github.com/lzA6/FreeAIchat-2api/pulls)**: 成为项目的贡献者，让你的名字永远镌刻在这里。
-   **点亮一颗 Star [<sup>7</sup>](https://github.com/lzA6/FreeAIchat-2api/stargazers)**: 这是对我们最大的鼓励和认可！

**世界不是由少数英雄改变的，而是由无数个像你我一样，愿意分享、愿意动手的普通人共同塑造的。来吧，朋友，让我们一起，玩得开心，创造不同！**

[license-shield]: https://img.shields.io/github/license/lzA6/FreeAIchat-2api.svg?style=for-the-badge
[license-url]: https://github.com/lzA6/FreeAIchat-2api/blob/main/LICENSE
[stars-shield]: https://img.shields.io/github/stars/lzA6/FreeAIchat-2api.svg?style=for-the-badge
[stars-url]: https://github.com/lzA6/FreeAIchat-2api/stargazers
[contributors-shield]: https://img.shields.io/github/contributors/lzA6/FreeAIchat-2api.svg?style=for-the-badge
[contributors-url]: https://github.com/lzA6/FreeAIchat-2api/graphs/contributors
[status-shield]: https://img.shields.io/badge/status-stable-green.svg?style=for-the-badge
[status-url]: #
