import json
import asyncio
import httpx
from httpx import AsyncClient, TimeoutException, HTTPStatusError, RemoteProtocolError
from ncatbot.plugin import BasePlugin, CompatibleEnrollment
from ncatbot.core.message import GroupMessage, PrivateMessage
from ncatbot.core.element import MessageChain, Image

bot = CompatibleEnrollment


class ImageSearchPlugin(BasePlugin):
    name = "ImageSearchPlugin"
    version = "1.0.0"
    requirements = ["httpx>=0.25.0"]

    async def on_load(self):
        self.register_config("max_images", "30")
        self.register_config(
            "r18_mapping", json.dumps({"冲一发": 0, "冲两发": 2, "冲三发": 1})
        )
        self.register_config("max_retries", "3")  # 新增重试次数配置

    @bot.group_event()
    async def on_group_message(self, msg: GroupMessage):
        await self.handle_message(msg)

    @bot.private_event()
    async def on_private_message(self, msg: PrivateMessage):
        await self.handle_message(msg)

    async def handle_message(self, msg):
        if isinstance(msg, GroupMessage):
            parts = msg.raw_message.split(maxsplit=1)
        else:
            parts = msg.raw_message.split(maxsplit=1)

        if not parts:
            return

        command = parts[0].lower()
        if command not in ["冲一发", "冲两发", "冲三发"]:
            return

        try:
            await self.handle_image_search(msg, command, parts)
        except Exception as e:
            if isinstance(msg, GroupMessage):
                await self.api.post_group_msg(
                    msg.group_id, text=f"图片搜索失败: {str(e)}"
                )
            else:
                await self.api.post_private_msg(
                    msg.user_id, text=f"图片搜索失败: {str(e)}"
                )
            await self.api.post_group_msg(msg.group_id, text="图片服务暂时不可用")

    async def handle_image_search(self, msg, command, parts):
        r18_mapping = json.loads(self.data["config"]["r18_mapping"])
        max_images = int(self.data["config"]["max_images"])
        max_retries = int(self.data["config"]["max_retries"])  # 获取最大重试次数

        r18_level = r18_mapping[command]
        params = parts[1].split() if len(parts) > 1 else []

        num = 1
        if params and params[0].isdigit():
            num = min(int(params[0]), max_images)
            keywords = params[1:]
        else:
            keywords = params

        base_url = (
            f"https://image.anosu.top/pixiv/json?size=regular&num={num}&r18={r18_level}"
        )
        if keywords:
            base_url += f"&keyword={'|'.join(keywords)}"

        for attempt in range(3):
            try:
                async with AsyncClient(
                    follow_redirects=True,
                    timeout=60,  # 增加超时时间
                    limits=httpx.Limits(max_connections=10),
                ) as client:
                    response = await client.get(base_url)
                    response.raise_for_status()
                    data = response.json()

                    valid_urls = await self.validate_urls(client, data, max_retries)

                    if not valid_urls:
                        if isinstance(msg, GroupMessage):
                            await self.api.post_group_msg(
                                msg.group_id, text="未找到符合条件的图片"
                            )
                        else:
                            await self.api.post_private_msg(
                                msg.user_id, text="未找到符合条件的图片"
                            )
                        return

                    batch_size = 1
                    for i in range(0, len(valid_urls), batch_size):
                        batch = valid_urls[i : i + batch_size]
                        if batch:
                            if isinstance(msg, GroupMessage):
                                await self.api.post_group_msg(
                                    msg.group_id,
                                    rtf=MessageChain([Image(url) for url in batch]),
                                )
                            else:
                                await self.api.post_private_msg(
                                    msg.user_id,
                                    rtf=MessageChain([Image(url) for url in batch]),
                                )
                    return

            except (TimeoutException, RemoteProtocolError, HTTPStatusError) as e:
                if attempt == 2:
                    raise
                await asyncio.sleep(2 ** (attempt + 1))

            except json.JSONDecodeError:
                raise

    async def validate_urls(self, client, data_list, max_retries):
        semaphore = asyncio.Semaphore(5)
        tasks = []
        for item in data_list:
            url = item.get("url")
            if url:
                tasks.append(self.check_url_with_retry(client, url, semaphore, max_retries))
        results = await asyncio.gather(*tasks)
        return [url for url in results if url]

    async def check_url_with_retry(self, client, url, semaphore, max_retries):
        async with semaphore:
            for retry in range(max_retries):
                try:
                    resp = await client.head(url, timeout=15)
                    if resp.status_code == 200:
                        return url
                except (TimeoutException, RemoteProtocolError, HTTPStatusError) as e:
                    if retry == max_retries - 1:
                        self._log.error(f"URL请求失败: {str(e)} URL: {url}")
                        return None
                    await asyncio.sleep(1)
            return None