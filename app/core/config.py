from pydantic_settings import BaseSettings
from typing import List, Optional, Dict

class Settings(BaseSettings):
    """
    应用配置 (v1.8 - 精确模型映射版)
    - 根据最终确认的情报，精确更新了模型名称到 bot_id 的映射。
    """
    # --- 应用元数据 ---
    APP_NAME: str = "FreeAIchat-2api"
    APP_VERSION: str = "1.8.0"
    DESCRIPTION: str = "一个将 chatgptfree.ai 转换为兼容 OpenAI 格式 API 的高性能、多模型、支持长期对话的通用代理。"

    # --- 认证与安全 ---
    API_MASTER_KEY: Optional[str] = None

    # --- FreeAIchat API 核心凭证 (全部从 .env 加载) ---
    COOKIE: str
    AJAX_NONCE: str
    SESSION_ID: str
    POST_ID: str

    # --- 模型名称到 bot_id 的映射表 (根据您的最终情报精确更新) ---
    MODEL_MAP: Dict[str, str] = {
        "gpt-4o-mini": "25865",
        "gpt-5-nano": "25871",
        "gemini-pro": "25874",
        "deepseek-coder": "25873",
        "claude-3-opus": "25875",
        "grok-1": "25872",
        "meta-llama-3": "25870",
        "qwen-max": "25869",
    }

    # --- 支持的模型列表 (根据上面的映射表自动生成) ---
    @property
    def SUPPORTED_MODELS(self) -> List[str]:
        return list(self.MODEL_MAP.keys())

    # --- Nginx 端口 ---
    NGINX_PORT: int = 8080

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"

settings = Settings()
