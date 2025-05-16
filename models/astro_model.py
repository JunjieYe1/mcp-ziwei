from iztro import Astro
from datetime import datetime
from utils.logger import Logger
from config.settings import Settings

class AstroModel:
    def __init__(self):
        self.astro = Astro()
        self.result = None
        self.horoscope_data = None
        self.settings = Settings()
        self.logger = Logger()
    
    def create_chart(self, birth_date, birth_time, gender):
        """创建命盘"""
        try:
            self.result = self.astro.by_solar(birth_date, birth_time, gender)
            return True
        except Exception as e:
            self.logger.error(f"创建命盘失败: {str(e)}")
            return False
    
    def get_horoscope(self, target_date, time_index):
        """获取运限信息"""
        try:
            if not self.result:
                self.logger.error("命盘未创建，无法获取运限信息")
                return False
            
            self.horoscope_data = self.result.horoscope(date=target_date, time_index=time_index)
            return True
        except Exception as e:
            self.logger.error(f"获取运限信息失败: {str(e)}")
            return False
    
    def get_chart_data(self):
        """获取命盘数据"""
        if not self.result:
            self.logger.warning("命盘未创建，无法获取数据")
            return None
        return self.result.model_dump(by_alias=True)
    
    def get_horoscope_data(self):
        """获取运限数据"""
        if not self.horoscope_data:
            self.logger.warning("运限信息未获取，无法获取数据")
            return None
        return self.horoscope_data.model_dump(by_alias=True) 