# Noupe-local/app/providers/base_provider.py

from abc import ABC, abstractmethod
from typing import Dict, Any, AsyncGenerator, Union
from fastapi import Request
from fastapi.responses import StreamingResponse, JSONResponse

class BaseProvider(ABC):
    """
    所有 Provider 的抽象基类。
    定义了处理聊天补全请求必须实现的核心方法。
    """

    @abstractmethod
    async def chat_completion(
        self,
        request_data: Dict[str, Any],
        original_request: Request
    ) -> Union[StreamingResponse, JSONResponse]:
        """
        处理聊天补全请求的核心方法。
        必须能够处理流式（StreamingResponse）和非流式（JSONResponse）两种情况。
        """
        pass
