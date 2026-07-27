# AI Shell

用自然语言生成并执行 Shell 命令，基于 DeepSeek API。

## 安装

1. 克隆仓库
2. 安装依赖：`pip install httpx`
3. 设置 API Key：

```bash
# CMD
setx DEEPSEEK_API_KEY "你的API密钥"

# Bash
export DEEPSEEK_API_KEY="你的API密钥"
```

4. 将项目目录加入 PATH，或使用提供的入口脚本：
   - **CMD/PowerShell**: 运行 `ai.cmd`
   - **Git Bash**: 运行 `ai`

## 使用

```bash
ai 显示当前时间
ai 列出当前目录下所有py文件
ai 创建一个名为test的文件夹
```

## 说明

- 仅支持 Windows（CMD / PowerShell / Git Bash）
- 当前 Git Bash 下存在 httpx 编码兼容问题，建议在 PowerShell 中使用
