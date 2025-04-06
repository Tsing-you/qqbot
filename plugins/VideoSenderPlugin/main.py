from ncatbot.plugin import BasePlugin, CompatibleEnrollment
from ncatbot.core.message import GroupMessage, PrivateMessage
import httpx
import asyncio

bot = CompatibleEnrollment

class VideoSenderPlugin(BasePlugin):
    name = "VideoSender"
    version = "1.0.1"  # 更新版本号
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_groups = [
                            #   561960789, 
                            #   2167033211, 
                               561476390
                              ]  # 指定自动发送的群组ID

    async def on_load(self):
        # 注册群聊和私聊事件处理
        self.register_handler("ncatbot.group_message_event", self.handle_group_message)
        self.register_handler("ncatbot.private_message_event", self.handle_private_message)
        print(f"{self.name} 插件已加载")

        # 注册定时任务，每60秒执行一次
        def sync_wrapper():
            asyncio.create_task(self.send_video())

        self.add_scheduled_task(
            job_func=sync_wrapper,
            name="定时发送视频",
            interval="3600s",  # 每3600秒执行一次
            max_runs=None
        )

    async def fetch_video_url(self):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get("https://api.dwo.cc/api/ksvideo")
                if resp.is_redirect:  # 检测到302重定向
                    video_url = resp.headers.get('location')
                    return video_url
                elif resp.status_code == 200:
                    data = resp.json()  # 简化json解析方式
                    return data.get('data', {}).get('video_url')
        except Exception as e:
            print(f"获取视频失败: {str(e)}")
        return None

    async def send_video(self):
        """定时任务的回调函数，用于发送视频"""
        for group_id in self.target_groups:
            try:
                video_url = await self.fetch_video_url()
                if video_url:
                    await self.api.post_group_file(
                        group_id=group_id,
                        video=video_url
                    )
                    print(f"成功自动发送视频到群组 {group_id}")
                else:
                    print(f"无法获取视频，跳过群组 {group_id}")
            except Exception as e:
                print(f"自动发送视频到群组 {group_id} 失败: {str(e)}")

    async def handle_group_message(self, event):
        msg = event.data
        if isinstance(msg, GroupMessage) and msg.raw_message.strip() == "来点视频":
            video_url = await self.fetch_video_url()
            if video_url:
                await self.api.post_group_file(
                    group_id=msg.group_id,
                    video=video_url
                )
            else:
                await msg.reply(text="暂时没有视频哦，请稍后再试~")

    async def handle_private_message(self, event):
        msg = event.data
        if isinstance(msg, PrivateMessage) and msg.raw_message.strip() == "来点视频":
            video_url = await self.fetch_video_url()
            if video_url:
                await self.api.post_private_file(
                    user_id=msg.user_id,
                    video=video_url
                )
            else:
                await msg.reply(text="视频获取失败，请联系管理员")

    async def on_unload(self):
        print(f"{self.name} 插件已卸载")