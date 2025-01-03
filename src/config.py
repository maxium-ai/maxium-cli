from pydantic_settings import BaseSettings


class Config(BaseSettings):
    CLI_CONFIG_EXTENSION: str = 'maxium_config'
    STACKING_THRESHOLD: int = 300
    BASE_AUTO_STACKING_URL: str = "https://api.maxium.ai/v1/automations/stack"

def get_config() -> Config:
    return Config()

config = get_config()
