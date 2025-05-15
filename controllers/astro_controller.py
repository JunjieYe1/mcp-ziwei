from models.astro_model import AstroModel
from convert import convert_main_json_to_text, convert_horoscope_to_text

class AstroController:
    def __init__(self):
        self.model = AstroModel()
    
    def create_chart(self, birth_date, birth_time, gender):
        """创建命盘"""
        return self.model.create_chart(birth_date, birth_time, gender)
    
    def get_horoscope(self, target_date, time_index):
        """获取运限信息"""
        return self.model.get_horoscope(target_date, time_index)
    
    def get_chart_text(self):
        """获取命盘文本"""
        chart_data = self.model.get_chart_data()
        if not chart_data:
            return None
        return convert_main_json_to_text(chart_data)
    
    def get_horoscope_text(self, target_date):
        """获取运限文本"""
        horoscope_data = self.model.get_horoscope_data()
        if not horoscope_data:
            return None
        return convert_horoscope_to_text(
            horoscope_data,
            precision='hourly',
            target_date=target_date
        ) 