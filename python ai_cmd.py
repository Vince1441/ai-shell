import os
import sys
import json
import platform
import subprocess

import httpx


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

_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
_BASE_URL = "https://api.deepseek.com/v1/chat/completions"


def main() -> None:
    user_prompt = ' '.join(sys.argv[1:]).strip()
    if not user_prompt:
        print("用法: python ai_cmd.py <你的自然语言需求>")
        print("例如: python ai_cmd.py 列出当前目录下所有py文件")
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
                    "model": "deepseek-v4-flash",
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
