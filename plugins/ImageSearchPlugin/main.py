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
        """插件加载时初始化配置并注册事件"""
        # 注册消息事件处理
        self.register_handler("ncatbot.group_message_event", self.handle_message)
        self.register_handler("ncatbot.private_message_event", self.handle_message)

        # 配置初始化
        self.register_config("max_images", "30")
        self.register_config(
            "r18_mapping", json.dumps({"冲一发": 0, "冲两发": 2, "冲三发": 1})
        )
        self.register_config("max_retries", "3")  # 新增重试次数配置

        print(f"{self.name} v{self.version} 已加载")

    async def handle_message(self, event):
        """统一的消息处理入口"""
        msg = event.data
        if not isinstance(msg, (GroupMessage, PrivateMessage)):
            return

        parts = msg.raw_message.split(maxsplit=1)
        if not parts:
            return

        command = parts[0].lower()
        if command not in ["冲一发", "冲两发", "冲三发"]:
            return

        try:
            await self.process_image_search(msg, command, parts)
        except Exception as e:
            await self.send_response(msg, f"图片搜索失败: {str(e)}")

    async def process_image_search(self, msg, command, parts):
        """核心图片搜索逻辑"""
        r18_mapping = json.loads(self.data["config"]["r18_mapping"])
        r18_level = r18_mapping[command]
        max_images = int(self.data["config"]["max_images"])
        max_retries = int(self.data["config"]["max_retries"])

        params = parts[1].split() if len(parts) > 1 else []
        num = 1
        if params and params[0].isdigit():
            num = min(int(params[0]), max_images)
            keywords = params[1:]
        else:
            keywords = params

        valid_urls = []
        remaining = num

        while remaining > 0 and remaining <= max_images:
            try:
                headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Referer": "https://image.anosu.top/"
}

                async with AsyncClient(
                    headers=headers,
                    follow_redirects=True,
                    timeout=60,
                    limits=httpx.Limits(max_connections=10)
                ) as client:
                    base_url = f"https://image.anosu.top/pixiv/json?size=regular&num={remaining}&r18={r18_level}"
                    if keywords:
                        base_url += f"&keyword={'|'.join(keywords)}"

                    response = await client.get(base_url)
                    response.raise_for_status()
                    data = response.json()

                    batch_valid_urls = await self.validate_urls(client, data, max_retries)
                    valid_urls.extend(batch_valid_urls)
                    remaining = num - len(valid_urls)

            except (TimeoutException, RemoteProtocolError, HTTPStatusError) as e:
                # self._log.error(f"图片请求失败: {str(e)}")
                break

            except json.JSONDecodeError:
                # self._log.error("图片数据解析失败")
                break

        if not valid_urls:
            await self.send_response(msg, "未找到符合条件的图片")
            return

        for batch in [valid_urls[i:i+1] for i in range(0, len(valid_urls), 1)]:
            if isinstance(msg, GroupMessage):
                await self.api.post_group_msg(
                    msg.group_id,
                    rtf=MessageChain([Image(url) for url in batch])
                )
            else:
                await self.api.post_private_msg(
                    msg.user_id,
                    rtf=MessageChain([Image(url) for url in batch])
                )

    async def validate_urls(self, client, data_list, max_retries):
        """并发验证图片URL有效性"""
        semaphore = asyncio.Semaphore(5)
        tasks = []
        for item in data_list:
            url = item.get("url")
            if url:
                tasks.append(self.check_url_with_retry(client, url, semaphore, max_retries))
        results = await asyncio.gather(*tasks)
        return [url for url in results if url]

    async def check_url_with_retry(self, client, url, semaphore, max_retries):
        """带重试机制的URL验证"""
        async with semaphore:
            for retry in range(max_retries):
                try:
                    resp = await client.head(url, timeout=15)
                    if resp.status_code == 200:
                        return url
                except (TimeoutException, RemoteProtocolError, HTTPStatusError) as e:
                    # if retry == max_retries - 1:
                    #     self._log.error(f"URL请求失败: {str(e)} URL: {url}")
                    await asyncio.sleep(1)
            return None

    async def send_response(self, msg, content):
        """统一消息发送逻辑"""
        if isinstance(msg, GroupMessage):
            await self.api.post_group_msg(msg.group_id, text=content)
        else:
            await self.api.post_private_msg(msg.user_id, text=content)

    async def on_unload(self):
        """插件卸载时触发"""
        print(f"{self.name} 插件已卸载")