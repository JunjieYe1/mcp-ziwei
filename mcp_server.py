import argparse
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from mcp.server import Server
from presenters.astro_presenter import AstroPresenter
import logging
import uvicorn
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 定义服务器名称
MCP_SERVER_NAME = "ziwei-server"

# 配置日志
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(MCP_SERVER_NAME)

# 初始化 FastMCP 实例
mcp = FastMCP(MCP_SERVER_NAME)

# 创建紫微斗数展示器实例
presenter = AstroPresenter()

# 定义工具
@mcp.tool()
def create_chart(birth_date: str, birth_time: int, gender: str, target_date: str | None = None) -> str:
    """
    创建紫微斗数命盘。

    参数：
    - birth_date (str): 出生日期，格式为 YYYY-MM-DD
    - birth_time (int): 出生时辰，0-12，其中0为早子时，1为丑时，2为寅时，3为卯时，4为辰时，5为巳时，6为午时，7为未时，8为申时，9为酉时，10为戌时，11为亥时，12为晚子时
    - gender (str): 性别，'M' 或 'F'
    - target_date (str, optional): 目标日期，格式为 YYYY-MM-DD。如果不提供，则只返回命盘信息。

    返回：
    - str: 命盘信息，如果提供了目标日期，则还会返回运势信息
    """
    try:
        # 创建命盘
        chart = presenter.create_chart(birth_date, birth_time, gender)
        if not chart:
            return "创建命盘失败"

        # 如果提供了目标日期，获取运势信息
        if target_date:
            horoscope = presenter.get_horoscope(chart, target_date)
            if not horoscope:
                return "获取运势信息失败"
            return f"命盘信息：\n{chart}\n\n运势信息：\n{horoscope}"
        
        return f"命盘信息：\n{chart}"
    except Exception as e:
        logger.error(f"创建命盘时发生错误: {str(e)}")
        return f"发生错误: {str(e)}"

# 创建 Starlette 应用
def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

# 主程序入口
if __name__ == "__main__":
    try:
        mcp_server = mcp._mcp_server

        # 解析命令行参数
        parser = argparse.ArgumentParser(description='Run MCP SSE-based server')
        parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
        parser.add_argument('--port', type=int, default=5173, help='Port to listen on')
        args = parser.parse_args()

        logger.info(f"Starting server on {args.host}:{args.port}")

        # 创建并运行 Starlette 应用
        starlette_app = create_starlette_app(mcp_server, debug=True)
        
        # 配置 uvicorn
        config = uvicorn.Config(
            app=starlette_app,
            host=args.host,
            port=args.port,
            log_level="debug",
            access_log=True,
            use_colors=False
        )
        
        # 启动服务器
        server = uvicorn.Server(config)
        server.run()
    except Exception as e:
        logger.error(f"服务器启动失败: {str(e)}")
        sys.exit(1) 