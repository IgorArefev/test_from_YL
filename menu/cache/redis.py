import json
from typing import Any

import aioredis
from fastapi.encoders import jsonable_encoder

from menu.core.config import settings


class Cache:
    """Клас для работы с кэшем."""

    def __init__(self):
        self.redis_client = aioredis.StrictRedis(
            host=settings.redis_server,
            port=settings.redis_port,
            db=settings.redis_db
        )

    async def get(self, key: str):
        """Получаем данные из базы по ключу."""
        cached_data = await self.redis_client.get(key)
        if cached_data:
            return cached_data.decode('utf-8')
        return None

    async def set(self, key: str, value: Any):
        """Записываем пару ключ-значение."""
        await self.redis_client.set(key, value)

    async def cache_or_data(
            self,
            key: str,
            _function: Any,
            *args: Any,
            **kwargs: Any,
    ):
        """
        Забираем кэш, если он есть,
        иначе записываем свежий кэш.
        """

        cached_result = await self.get(key)
        if cached_result:
            return json.loads(cached_result)

        items = await _function(*args, **kwargs)
        json_data = jsonable_encoder(items)
        await self.set(key, json.dumps(json_data))
        return items

    async def invalidate(self, *args: str):
        """Очистка кэша."""
        for cache_key in args:
            await self.redis_client.delete(cache_key)


redis_cache = Cache()
