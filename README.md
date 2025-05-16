# 紫微斗数 MCP 服务

这是一个基于 MCP（Model Context Protocol）的紫微斗数命盘计算服务。它提供了一个简单的接口来计算和显示紫微斗数命盘和运限信息。

## 安装

1. 确保您已安装 Python 3.8 或更高版本

2. 安装 uv 包管理器：
   ```powershell
   # Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
   ```bash
   # Linux/MacOS
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. 克隆此仓库并进入项目目录

4. 创建并激活虚拟环境：
   ```powershell
   # Windows
   uv venv
   .venv\Scripts\activate
   ```
   ```bash
   # Linux/MacOS
   uv venv
   source .venv/bin/activate
   ```

5. 安装依赖：
   ```powershell
   pip install -e .
   ```

## 使用方法

### 使用 MCP Inspector 进行测试

1. 运行 MCP 服务器（选择以下任一方式）：
   ```powershell
   # 方式1：使用 mcp 命令
   mcp dev mcp_server.py
   
   # 方式2：直接运行 Python 文件
   python mcp_server.py
   ```
2. 打开 http://localhost:5173/ 进行功能测试

### 在 Cursor 中使用

1. 打开 Cursor 设置
2. 进入 MCP 设置页面
3. 点击 "Add new MCP server"
4. 选择类型为 "command"
5. 设置命令为（选择以下任一方式）：
   ```powershell
   # 方式1：使用 mcp 命令
   mcp dev mcp_server.py
   
   # 方式2：直接运行 Python 文件
   python mcp_server.py
   ```

### 在 Cline 中使用

在 Cline 的配置文件中添加（选择以下任一方式）：

```json
{
    "mcpServers": {
        "ziwei": {
            "command": "mcp",
            "args": [
                "dev",
                "mcp_server.py"
            ]
        }
    }
}
```

或者

```json
{
    "mcpServers": {
        "ziwei": {
            "command": "python",
            "args": [
                "mcp_server.py"
            ]
        }
    }
}
```

## 功能

### create_chart

创建并显示紫微斗数命盘和运限信息。

参数：
- `birth_date`: 出生日期，格式为 YYYY-MM-DD
- `birth_time`: 出生时辰，0-12 的整数
- `gender`: 性别，可选值为"男"或"女"
- `target_date`: 目标日期，格式为 YYYY-MM-DD，用于计算运限信息

返回：
- 包含命盘和运限信息的文本描述

## 示例

```python
result = create_chart(
    birth_date="1996-09-12",
    birth_time=9,
    gender="男",
    target_date="2025-05-15"
)
print(result)
``` 