from ncatbot.plugin import BasePlugin, CompatibleEnrollment
from ncatbot.core.message import GroupMessage, PrivateMessage
import httpx
import json

bot = CompatibleEnrollment

class TestPlugin(BasePlugin):
    name = "Tesyplugin"
    version = "1.0.0"
    
    async def on_load(self):
        # 注册群聊和私聊事件处理
        self.register_handler("ncatbot.group_message_event", self.handle_group_message)
        self.register_handler("ncatbot.private_message_event", self.handle_private_message)
        print(f"{self.name} 插件已加载")

    async def handle_group_message(self, event):
        msg = event.data
        if isinstance(msg, GroupMessage) and msg.raw_message.strip() == "测试":
                await self.api.post_group_msg(
                    group_id=msg.group_id,
                    text="测试成功"
                )

    async def handle_private_message(self, event):
        msg = event.data
        if isinstance(msg, PrivateMessage) and msg.raw_message.strip() == "测试":
                await self.api.post_private_msg(
                    user_id=msg.user_id,
                    text="测试成功"
                )

    async def on_unload(self):
        print(f"{self.name} 插件已卸载")