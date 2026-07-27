# AI Shell

用自然语言生成并执行 Shell 命令，支持多种大模型 API。

## 安装

1. 克隆仓库
2. 安装依赖：`pip install httpx`
3. 设置 API Key（根据使用的提供商选择）：

```cmd
rem DeepSeek（默认）
setx DEEPSEEK_API_KEY "你的密钥"

rem OpenAI
setx OPENAI_API_KEY "你的密钥"

rem 通义千问
setx DASHSCOPE_API_KEY "你的密钥"

rem 智谱 GLM
setx ZHIPU_API_KEY "你的密钥"

rem Moonshot
setx MOONSHOT_API_KEY "你的密钥"
```

4. 将项目目录加入 PATH，或直接使用 `ai.cmd`

## 切换模型

通过 `AI_PROVIDER` 环境变量切换：

```cmd
set AI_PROVIDER=openai       rem 切换到 OpenAI
set AI_PROVIDER=qwen         rem 切换到通义千问
set AI_PROVIDER=zhipu        rem 切换到智谱 GLM
set AI_PROVIDER=moonshot     rem 切换到 Moonshot
```

不设置则默认使用 DeepSeek。

### 自定义 API

```cmd
set AI_BASE_URL=https://your-api.com/v1/chat/completions
set AI_MODEL=your-model-name
set AI_API_KEY=your-key
```

## 使用

```cmd
ai 显示当前时间
ai 列出当前目录下所有py文件
ai 创建一个名为test的文件夹
```

## 说明

- 支持 Windows CMD 和 PowerShell
- 如需全局使用，将项目目录添加到系统 PATH 环境变量
