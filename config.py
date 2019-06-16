import yaml

class Config:
    def __init__(self, config_path):
        with open(config_path) as f:
            self.config_dict = yaml.safe_load(f.read())
            self.units = self.config_dict['Units']




