import os
import json

class Settings:
    def __init__(self):
        self.config = {
            'log_level': 'INFO',
            'log_dir': 'logs',
            'output_dir': 'output',
            'default_precision': 'hourly',
            'date_format': '%Y-%m-%d',
            'time_format': '%H:%M:%S'
        }
        self.load_config()
    
    def load_config(self):
        """从配置文件加载配置"""
        config_file = os.path.join(os.path.dirname(__file__), 'config.json')
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
            except Exception as e:
                print(f"加载配置文件失败: {str(e)}")
    
    def save_config(self):
        """保存配置到文件"""
        config_file = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存配置文件失败: {str(e)}")
    
    def get(self, key, default=None):
        """获取配置项"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """设置配置项"""
        self.config[key] = value
        self.save_config() 