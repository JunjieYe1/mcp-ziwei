from controllers.astro_controller import AstroController

class AstroPresenter:
    def __init__(self):
        self.controller = AstroController()
    
    def create_and_show_chart(self, birth_date, birth_time, gender, target_date):
        """创建并显示命盘和运限信息"""
        # 创建命盘
        if not self.controller.create_chart(birth_date, birth_time, gender):
            return "创建命盘失败"
        
        # 获取运限信息
        if not self.controller.get_horoscope(target_date, birth_time):
            return "获取运限信息失败"
        
        # 获取命盘文本
        chart_text = self.controller.get_chart_text()
        if not chart_text:
            return "获取命盘文本失败"
        
        # 获取运限文本
        horoscope_text = self.controller.get_horoscope_text(target_date)
        if not horoscope_text:
            return "获取运限文本失败"
        
        # 组合输出
        output = []
        output.append("=== 命盘信息 ===")
        output.append(chart_text)
        output.append("\n=== 运限信息 ===")
        output.append(horoscope_text)
        
        return "\n".join(output) 