import traceback
import time
import uuid
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, Request, HTTPException, Depends, Header
from app.core.config import settings
from app.providers.freeaichat_provider import FreeaichatProvider, CONVERSATION_CONTEXT
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.DESCRIPTION
)

provider = FreeaichatProvider()

async def verify_api_key(authorization: Optional[str] = Header(None)):
    """
    验证 API 密钥的依赖项 (v1.6 健壮版)。
    """
    if settings.API_MASTER_KEY:
        if authorization is None:
            logger.warning("请求缺少 Authorization 头部，但已配置 API_MASTER_KEY。")
            raise HTTPException(
                status_code=401,
                detail="Unauthorized: Missing Authorization header.",
            )
        
        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise ValueError("Invalid scheme")
        except ValueError:
            logger.warning(f"无效的认证格式: {authorization}")
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication scheme. Use 'Bearer <your_api_key>'.",
            )
        
        if token != settings.API_MASTER_KEY:
            logger.warning(f"无效的 API Key: {token[:4]}... (与期望值不匹配)")
            raise HTTPException(
                status_code=403,
                detail="Forbidden: Invalid API Key.",
            )
        
        logger.info("API Key 验证通过。")

@app.post("/v1/conversations", dependencies=[Depends(verify_api_key)])
async def create_conversation():
    """
    创建一个新的会话容器，返回一个用于保持对话上下文的 `conversation_id`。
    """
    conversation_id = str(uuid.uuid4())
    CONVERSATION_CONTEXT[conversation_id] = {
        "last_response_id": None,
        "conversation_uuid": str(uuid.uuid4())
    }
    logger.info(f"创建新会话，ID: {conversation_id}")
    return {"conversation_id": conversation_id}

@app.post("/v1/chat/completions", dependencies=[Depends(verify_api_key)])
async def chat_completions(request: Request):
    """
    处理聊天请求。
    - **可选**: 在请求体中包含从 `/v1/conversations` 获取的 `conversation_id` 以进行长期对话。
    - **如果未提供 `conversation_id`**，将作为一次性对话处理。
    - **可选**: 在请求体中加入 `"web_search": true` 来启用联网搜索功能。
    """
    try:
        request_data = await request.json()
        return await provider.chat_completion(request_data, request)
    except Exception as e:
        logger.error(f"处理聊天请求时发生错误: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/models", dependencies=[Depends(verify_api_key)])
async def list_models():
    """返回支持的模型列表。"""
    return {
        "object": "list",
        "data": [{"id": name, "object": "model", "created": int(time.time()), "owned_by": "system"} for name in settings.SUPPORTED_MODELS]
    }

@app.get("/")
def root():
    """根路由，提供服务基本信息。"""
    return {"message": f"Welcome to {settings.APP_NAME} v{settings.APP_VERSION}"}
