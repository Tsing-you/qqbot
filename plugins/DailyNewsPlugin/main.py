from ncatbot.plugin import BasePlugin
from ncatbot.core.message import GroupMessage
import asyncio

class DailyNewsPlugin(BasePlugin):
    name = "NewsSender"  # 插件名称
    version = "1.0.0"    # 插件版本

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_groups = [2167033211,561476390,561960789]  # 替换为您需要发送的群组ID
        self.image_url = "https://api.southerly.top/api/60s?format=image"  # 图片URL

    async def on_load(self):
        """插件加载时注册定时任务"""
        print(f"{self.name} 插件已加载")
        print(f"插件版本: {self.version}")

        # 注册定时任务，每15秒执行一次
        def sync_wrapper():
        # 在已有的事件循环中创建异步任务
            asyncio.create_task(self.send_news())

        self.add_scheduled_task(
            job_func=sync_wrapper,  # 改用同步包装器
            name="定时发送新闻",
            interval="86400s",     # 调整为24小时（避免频繁调用）
            max_runs=None
        )

    async def send_news(self):
        """定时任务的回调函数，用于发送消息"""
        for group_id in self.target_groups:
            try:
                # 发送消息到指定群组
                await self.api.post_group_msg(
                    group_id=group_id,
                    text="嗷呜酱每日新闻送达！",
                    image=self.image_url
                )
                print(f"成功发送消息到群组 {group_id}")
            except Exception as e:
                print(f"发送消息到群组 {group_id} 失败: {str(e)}")

    async def on_unload(self):
        """插件卸载时的清理工作"""
        print(f"{self.name} 插件已卸载")