import sys
import os
# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from presenters.astro_presenter import AstroPresenter

def main():
    try:
        # 创建展示器
        presenter = AstroPresenter()
        
        # 设置参数
        birth_date = "1996-09-12"
        birth_time = 9
        gender = "男"
        target_date = "2025-05-15"
        
        # 创建并显示命盘
        result = presenter.create_and_show_chart(
            birth_date=birth_date,
            birth_time=birth_time,
            gender=gender,
            target_date=target_date
        )
        
        print(result)
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        print(f"错误类型: {type(e).__name__}")

if __name__ == '__main__':
    main()
