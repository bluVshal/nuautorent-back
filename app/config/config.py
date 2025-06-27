from app.config.dev_config import DevConfig
from app.config.production_config import ProductionConfig


class Config:
    def __init__(self):
        self.dev_config = DevConfig()
        self.production_config = ProductionConfig()