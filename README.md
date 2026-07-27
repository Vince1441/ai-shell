# AI Shell

用自然语言生成并执行 Shell 命令，基于 DeepSeek API。

## 安装

1. 克隆仓库
2. 安装依赖：`pip install httpx`
3. 设置 API Key：

```cmd
setx DEEPSEEK_API_KEY "你的API密钥"
```

4. 将项目目录加入 PATH（参考下方说明），或直接使用 `ai.cmd`

## 使用

```cmd
ai 显示当前时间
ai 列出当前目录下所有py文件
ai 创建一个名为test的文件夹
```

## 说明

- 支持 Windows CMD 和 PowerShell
- 如需全局使用，将项目目录添加到系统 PATH 环境变量
