from typing import Any
from mcp.server.fastmcp import FastMCP
from presenters.astro_presenter import AstroPresenter

# 初始化 FastMCP 服务器
mcp = FastMCP("ziwei")

# 创建紫微斗数展示器实例
presenter = AstroPresenter()

@mcp.tool()
def create_chart(birth_date: str, birth_time: int, gender: str, target_date: str | None = None) -> str:
    """创建并显示紫微斗数命盘和运限信息。

    Args:
        birth_date: 出生日期，格式为 YYYY-MM-DD
        birth_time: 出生时辰，0-12 的整数，其中：
            0为早子时，1为丑时，2为寅时，3为卯时，4为辰时，5为巳时，6为午时，
            7为未时，8为申时，9为酉时，10为戌时，11为亥时，12为晚子时
        gender: 性别，可选值为"男"或"女"
        target_date: 目标日期，格式为 YYYY-MM-DD，用于计算运限信息。如果不提供，则只返回命盘信息。

    Returns:
        str: 包含命盘和运限信息的文本描述
    """
    try:
        result = presenter.create_and_show_chart(
            birth_date=birth_date,
            birth_time=birth_time,
            gender=gender,
            target_date=target_date
        )
        return result
    except Exception as e:
        return f"创建命盘失败: {str(e)}"

def main():
    """主函数，用于直接运行服务器"""
    mcp.run(transport='sse', host='0.0.0.0', port=5173)

if __name__ == "__main__":
    main() 