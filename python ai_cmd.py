import os
import sys
import platform
import subprocess

import httpx


# ── 模型提供商预设 ──────────────────────────────────────────
# 通过 AI_PROVIDER 环境变量切换，默认 deepseek
# 自定义模式：设置 AI_BASE_URL + AI_MODEL + AI_API_KEY 即可
_PROVIDERS = {
    "deepseek": {
        "base_url": "https://api.deepseek.com/v1/chat/completions",
        "model": "deepseek-v4-flash",
        "api_key_env": "DEEPSEEK_API_KEY",
    },
    "openai": {
        "base_url": "https://api.openai.com/v1/chat/completions",
        "model": "gpt-4o",
        "api_key_env": "OPENAI_API_KEY",
    },
    "qwen": {
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        "model": "qwen-plus",
        "api_key_env": "DASHSCOPE_API_KEY",
    },
    "zhipu": {
        "base_url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "model": "glm-4-flash",
        "api_key_env": "ZHIPU_API_KEY",
    },
    "moonshot": {
        "base_url": "https://api.moonshot.cn/v1/chat/completions",
        "model": "moonshot-v1-8k",
        "api_key_env": "MOONSHOT_API_KEY",
    },
}


def _resolve_config() -> tuple[str, str, str]:
    """解析配置，返回 (api_key, base_url, model)"""
    provider = os.environ.get("AI_PROVIDER", "").strip().lower()

    # 预设模式
    if provider in _PROVIDERS:
        cfg = _PROVIDERS[provider]
        api_key = os.environ.get(cfg["api_key_env"], "")
        return api_key, cfg["base_url"], cfg["model"]

    # 自定义模式
    base_url = os.environ.get("AI_BASE_URL", "")
    if base_url:
        api_key = os.environ.get("AI_API_KEY", "")
        model = os.environ.get("AI_MODEL", "gpt-3.5-turbo")
        return api_key, base_url, model

    # 向后兼容：未设置 AI_PROVIDER 也无 AI_BASE_URL，默认 deepseek
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    return api_key, _PROVIDERS["deepseek"]["base_url"], _PROVIDERS["deepseek"]["model"]


def _detect_shell() -> tuple[str, str | None]:
    """检测当前 Shell 环境，返回 (提示词描述, subprocess executable)"""
    system = platform.system()
    shell_env = os.environ.get("SHELL", "")
    msystem = os.environ.get("MSYSTEM", "")

    if system == "Windows":
        if "bash" in shell_env.lower() or msystem:
            return "bash（Windows 上的 Git Bash）", "bash"
        return "Windows CMD 或 PowerShell", None
    elif system == "Linux":
        return "bash", "bash"
    elif system == "Darwin":
        return "bash（macOS）", "bash"
    return "bash", "bash"


_SHELL_HINT, _EXECUTABLE = _detect_shell()

_SYSTEM_PROMPT = (
    "You are a shell command generator. Based on user's request, output a single executable command.\n"
    "Rules:\n"
    "1. Output ONLY the command itself, no explanation, no markdown code blocks\n"
    "2. If unable to understand or generate, output FAILED: reason\n"
    f"3. User is on {_SHELL_HINT}, generate commands accordingly"
)

_API_KEY, _BASE_URL, _MODEL = _resolve_config()


def main() -> None:
    user_prompt = ' '.join(sys.argv[1:]).strip()
    if not user_prompt:
        print("用法: ai <你的自然语言需求>")
        print("例如: ai 列出当前目录下所有py文件")
        sys.exit(1)

    if not _API_KEY:
        print("错误: 未设置 API Key 环境变量")
        print("请根据使用的提供商设置对应的环境变量，例如：")
        print("  DeepSeek:  setx DEEPSEEK_API_KEY \"你的密钥\"")
        print("  OpenAI:    setx OPENAI_API_KEY \"你的密钥\"")
        print("  通义千问:  setx DASHSCOPE_API_KEY \"你的密钥\"")
        print("  智谱:      setx ZHIPU_API_KEY \"你的密钥\"")
        print("  Moonshot:  setx MOONSHOT_API_KEY \"你的密钥\"")
        print("  自定义:    setx AI_API_KEY \"你的密钥\"")
        sys.exit(1)

    try:
        with httpx.Client(trust_env=False) as client:
            resp = client.post(
                _BASE_URL,
                headers={
                    "Authorization": f"Bearer {_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": _MODEL,
                    "messages": [
                        {"role": "system", "content": _SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0,
                },
                timeout=30,
            )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)

    cmd = data["choices"][0]["message"]["content"].strip()

    if cmd.startswith("FAILED:"):
        print(f"\033[91m[AI失败]: {cmd[7:].strip()}\033[0m")
        return

    print(f"\033[92m[AI命令]: {cmd}\033[0m")
    y_or_n = input("是否执行此命令？(y/N): ")
    if y_or_n.lower() == 'y':
        try:
            subprocess.run(cmd, shell=True, check=True, executable=_EXECUTABLE)
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败，返回码: {e.returncode}")
    else:
        print("已取消执行。")


if __name__ == "__main__":
    main()
