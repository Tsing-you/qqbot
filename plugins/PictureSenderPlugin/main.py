from ncatbot.plugin import BasePlugin, CompatibleEnrollment
from ncatbot.core.message import GroupMessage, PrivateMessage
import httpx
import asyncio
import json

bot = CompatibleEnrollment

class PictureSenderPlugin(BasePlugin):
    name = "PictureSender"
    version = "1.0.0"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_groups = [
            #   561960789,
            #   2167033211, 
               561476390
              ]  # 指定自动发送的群组ID
        self.headers = {
            'Authorization': 'bUmFQYagrRWWBBoG2nyTow'  # 替换为您的Token
        }
        self.api_url = "https://api.makuo.cc/api/get.img.tuwan"
        self.tags = [
            "女仆", "jk制服", "兔女郎", "夏日泳装", "动漫类", "萝莉", 
            "御姐", "巨乳", "丰满微胖", "黑丝", "白丝", "肉丝", 
            "网丝", "吊带袜", "腿控", "脚控", "旗袍"
        ]

    async def on_load(self):
        # 注册群聊和私聊事件处理
        self.register_handler("ncatbot.group_message_event", self.handle_group_message)
        self.register_handler("ncatbot.private_message_event", self.handle_private_message)
        print(f"{self.name} 插件已加载")

        # 注册定时任务，每1800秒执行一次
        def sync_wrapper():
            asyncio.create_task(self.send_picture())

        self.add_scheduled_task(
            job_func=sync_wrapper,
            name="定时发送图片",
            interval="1800s",  # 每1800秒执行一次
            max_runs=None
        )

    async def fetch_picture_url(self, sort=None):
        try:
            params = {}
            if sort:
                params["sort"] = sort
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.api_url,
                    headers=self.headers,
                    params=params
                )
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == 200:
                        return data.get("data", {}).get("url")
        except Exception as e:
            print(f"获取图片失败: {str(e)}")
        return None

    async def send_picture(self):
        """定时任务的回调函数，用于发送图片"""
        for group_id in self.target_groups:
            try:
                picture_url = await self.fetch_picture_url()
                if picture_url:
                    await self.api.post_group_msg(
                        group_id=group_id,
                        image=picture_url
                    )
                    print(f"成功自动发送图片到群组 {group_id}")
                else:
                    print(f"无法获取图片，跳过群组 {group_id}")
            except Exception as e:
                print(f"自动发送图片到群组 {group_id} 失败: {str(e)}")

    async def handle_group_message(self, event):
        msg = event.data
        if isinstance(msg, GroupMessage) and msg.raw_message.startswith("冲四发"):
            parts = msg.raw_message.split(maxsplit=1)
            sort = None
            if len(parts) > 1:
                sort = parts[1].strip()
                if sort not in self.tags:
                    await msg.reply(text=f"无效的标签，请选择以下标签之一：{', '.join(self.tags)}")
                    return
            picture_url = await self.fetch_picture_url(sort)
            if picture_url:
                await self.api.post_group_msg(
                    group_id=msg.group_id,
                    image=picture_url
                )
            else:
                await msg.reply(text="暂时没有图片哦，请稍后再试~")

    async def handle_private_message(self, event):
        msg = event.data
        if isinstance(msg, PrivateMessage) and msg.raw_message.startswith("冲四发"):
            parts = msg.raw_message.split(maxsplit=1)
            sort = None
            if len(parts) > 1:
                sort = parts[1].strip()
                if sort not in self.tags:
                    await msg.reply(text=f"无效的标签，请选择以下标签之一：{', '.join(self.tags)}")
                    return
            picture_url = await self.fetch_picture_url(sort)
            if picture_url:
                await self.api.post_private_msg(
                    user_id=msg.user_id,
                    image=picture_url
                )
            else:
                await msg.reply(text="暂时没有图片哦，请稍后再试~")

    async def on_unload(self):
        print(f"{self.name} 插件已卸载")