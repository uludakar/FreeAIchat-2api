import httpx
import json
import uuid
import time
import traceback
import asyncio
from typing import Dict, Any, AsyncGenerator, Union, List, Tuple, Optional

from fastapi import Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse

from app.providers.base_provider import BaseProvider
from app.core.config import settings

import logging
logger = logging.getLogger(__name__)

# 全局会话上下文存储容器
CONVERSATION_CONTEXT: Dict[str, Dict[str, Any]] = {}

def fix_encoding(text: str) -> str:
    """修复上游服务可能存在的双重编码或错误编码问题。"""
    try:
        return text.encode('latin-1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text

class FreeaichatProvider(BaseProvider):
    """
    FreeAIchat.ai 服务提供商 (v1.7)
    - 智能会话处理：当请求中不含 conversation_id 时，自动创建临时会话，实现对标准客户端的无缝兼容。
    """

    async def chat_completion(self, request_data: Dict[str, Any], original_request: Request) -> Union[StreamingResponse, JSONResponse]:
        is_temporary_conversation = False
        conversation_id = request_data.get("conversation_id")

        try:
            # --- 智能会话处理 ---
            if not conversation_id:
                is_temporary_conversation = True
                conversation_id = f"temp-{uuid.uuid4()}"
                CONVERSATION_CONTEXT[conversation_id] = {
                    "last_response_id": None,
                    "conversation_uuid": str(uuid.uuid4())
                }
                logger.info(f"未提供 conversation_id，创建临时会话: {conversation_id}")
            elif conversation_id not in CONVERSATION_CONTEXT:
                raise HTTPException(status_code=400, detail=f"无效的 'conversation_id': {conversation_id}。请确认 ID 是否正确，或通过 /v1/conversations 创建新会话。")

            context = CONVERSATION_CONTEXT[conversation_id]
            previous_response_id = context.get("last_response_id")
            conversation_uuid = context.get("conversation_uuid")

            model_name = request_data.get("model")
            if not model_name or model_name not in settings.MODEL_MAP:
                raise HTTPException(status_code=400, detail=f"不支持的模型: {model_name}。可用模型: {', '.join(settings.SUPPORTED_MODELS)}")
            
            bot_id = settings.MODEL_MAP[model_name]
            web_search = request_data.get("web_search", False)
            
            logger.info(f"会话ID: {conversation_id}, 模型: '{model_name}', bot_id: {bot_id}, 上一轮ID: {previous_response_id}, 联网搜索: {web_search}")

            cache_key = await self._get_cache_key(request_data, bot_id)
            if not cache_key:
                raise HTTPException(status_code=500, detail="未能从上游服务获取 cache_key。")

            is_stream = request_data.get("stream", False)
            stream_generator = self._stream_response(cache_key, bot_id, model_name, conversation_uuid, previous_response_id, web_search)

            async def response_generator():
                full_content = ""
                new_response_id = None
                chat_id = f"chatcmpl-{uuid.uuid4().hex}"

                if is_stream:
                    role_chunk = {"id": chat_id, "object": "chat.completion.chunk", "created": int(time.time()), "model": model_name, "choices": [{"index": 0, "delta": {"role": "assistant"}, "finish_reason": None}]}
                    yield f"data: {json.dumps(role_chunk, ensure_ascii=False)}\n\n"
                
                async for chunk_type, chunk_data in stream_generator:
                    if chunk_type == "content":
                        full_content += chunk_data
                        if is_stream:
                            delta_chunk = {"id": chat_id, "object": "chat.completion.chunk", "created": int(time.time()), "model": model_name, "choices": [{"index": 0, "delta": {"content": chunk_data}, "finish_reason": None}]}
                            yield f"data: {json.dumps(delta_chunk, ensure_ascii=False)}\n\n"
                    elif chunk_type == "response_id":
                        new_response_id = chunk_data
                
                if new_response_id and not is_temporary_conversation:
                    CONVERSATION_CONTEXT[conversation_id]["last_response_id"] = new_response_id
                    logger.info(f"会话 {conversation_id} 上下文已更新, 新的 response_id: {new_response_id}")

                if is_stream:
                    final_chunk = {"id": chat_id, "object": "chat.completion.chunk", "created": int(time.time()), "model": model_name, "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]}
                    yield f"data: {json.dumps(final_chunk, ensure_ascii=False)}\n\n"
                    yield "data: [DONE]\n\n"
                    logger.info("流式响应结束。")
                else:
                    yield full_content

            if is_stream:
                return StreamingResponse(response_generator(), media_type="text/event-stream")
            else:
                full_content = await response_generator().__anext__()
                return JSONResponse({
                    "id": f"chatcmpl-{uuid.uuid4().hex}",
                    "object": "chat.completion",
                    "created": int(time.time()),
                    "model": model_name,
                    "choices": [{"index": 0, "message": {"role": "assistant", "content": full_content.strip()}, "finish_reason": "stop"}],
                    "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                })

        except Exception as e:
            logger.error(f"处理 FreeAIchat 请求时出错: {type(e).__name__}: {e}")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"处理 FreeAIchat 请求时发生内部错误: {e}")
        
        finally:
            # 如果是临时会话，结束后立即清理
            if is_temporary_conversation and conversation_id in CONVERSATION_CONTEXT:
                del CONVERSATION_CONTEXT[conversation_id]
                logger.info(f"临时会话 {conversation_id} 已清理。")

    async def _get_cache_key(self, request_data: Dict[str, Any], bot_id: str) -> str:
        url = "https://chatgptfree.ai/wp-admin/admin-ajax.php"
        headers = self._prepare_headers(is_stream=False)
        last_user_message = next((msg["content"] for msg in reversed(request_data.get("messages", [])) if msg["role"] == "user"), "")
        if not last_user_message:
            raise ValueError("请求中未找到用户消息。")
        form_data = {
            'action': 'aipkit_cache_sse_message',
            'message': last_user_message,
            '_ajax_nonce': settings.AJAX_NONCE,
            'bot_id': bot_id,
            'user_client_message_id': f'aipkit-client-msg-{bot_id}-{int(time.time() * 1000)}-{uuid.uuid4().hex[:5]}'
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, data=form_data)
            response.raise_for_status()
            response_json = response.json()
            if response_json.get("success") and response_json.get("data", {}).get("cache_key"):
                cache_key = response_json["data"]["cache_key"]
                logger.info(f"成功获取 cache_key: {cache_key}")
                return cache_key
            else:
                logger.error(f"获取 cache_key 失败: {response_json}")
                return ""

    async def _stream_response(self, cache_key: str, bot_id: str, model_name: str, conversation_uuid: str, previous_response_id: Optional[str], web_search: bool) -> AsyncGenerator[Tuple[str, str], None]:
        url = "https://chatgptfree.ai/wp-admin/admin-ajax.php"
        params = {
            'action': 'aipkit_frontend_chat_stream',
            'cache_key': cache_key,
            'bot_id': bot_id,
            'session_id': settings.SESSION_ID,
            'conversation_uuid': conversation_uuid,
            'post_id': settings.POST_ID,
            '_ts': int(time.time() * 1000),
            '_ajax_nonce': settings.AJAX_NONCE
        }
        if previous_response_id:
            params['previous_openai_response_id'] = previous_response_id
        if web_search:
            params['frontend_web_search_active'] = 'true'
        
        headers = self._prepare_headers(is_stream=True)

        async with httpx.AsyncClient(timeout=180) as client:
            async with client.stream("GET", url, headers=headers, params=params) as response:
                response.raise_for_status()
                
                buffer = ""
                async for line in response.aiter_lines():
                    buffer += line + "\n"
                    if buffer.endswith("\n\n"):
                        events = buffer.strip().split("\n\n")
                        for event_str in events:
                            if not event_str: continue
                            
                            event_lines = event_str.split("\n")
                            event_type = "message"
                            data_lines = []

                            for eline in event_lines:
                                if eline.startswith("event:"):
                                    event_type = eline[len("event:"):].strip()
                                elif eline.startswith("data:"):
                                    data_lines.append(eline[len("data:"):].strip())
                            
                            data_str = "".join(data_lines)

                            if event_type == "openai_response_id":
                                try:
                                    data_json = json.loads(data_str)
                                    new_id = data_json.get("id")
                                    if new_id:
                                        yield "response_id", new_id
                                except json.JSONDecodeError:
                                    logger.warning(f"无法解析 openai_response_id 数据: {data_str}")
                            elif data_str:
                                try:
                                    if data_str == "[DONE]": continue
                                    data_json = json.loads(data_str)
                                    delta_content = data_json.get("delta")
                                    if isinstance(delta_content, str):
                                        yield "content", fix_encoding(delta_content)
                                except json.JSONDecodeError:
                                    logger.warning(f"无法解析 SSE 数据块: {data_str}")
                        buffer = ""

    def _prepare_headers(self, is_stream: bool = False) -> Dict[str, str]:
        if not settings.COOKIE:
            raise ValueError("COOKIE 未在 .env 文件中配置。")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
            "Referer": "https://chatgptfree.ai/",
            "Origin": "https://chatgptfree.ai",
            "Cookie": settings.COOKIE
        }
        if is_stream:
            headers.update({"Accept": "text/event-stream", "Cache-Control": "no-cache"})
        else:
            headers["Accept"] = "*/*"
        return headers
