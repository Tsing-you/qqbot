from ncatbot.plugin import BasePlugin
from ncatbot.core.message import GroupMessage, PrivateMessage
from ncatbot.utils.logger import get_log

_log = get_log()

class HelpPlugin(BasePlugin):
    name = "HelpPlugin"
    version = "1.0.0"

    async def on_load(self):
        self.register_handler("ncatbot.group_message_event", self.handle_group_message)
        self.register_handler("ncatbot.private_message_event", self.handle_private_message)
        print(f"{self.name} 插件已加载")

    async def handle_group_message(self, event):
        msg = event.data
        if isinstance(msg, GroupMessage) and msg.raw_message.strip() == "说明":
            help_text = self.generate_help_text()
            await self.api.post_group_msg(
                group_id=msg.group_id,
                text=help_text
            )

    async def handle_private_message(self, event):
        msg = event.data
        if isinstance(msg, PrivateMessage) and msg.raw_message.strip() == "说明":
            help_text = self.generate_help_text()
            await self.api.post_private_msg(
                user_id=msg.user_id,
                text=help_text
            )

    def generate_help_text(self):
        return """**
**QQ机器人功能说明**

1. **生成图片**
- 示例: `冲一发 2 ロリ`

2. **AI对话**
- 示例: `ai 介绍你自己`

3. **角色扮演**
- 示例: `角色扮演 猫娘`
- 提示: 角色扮演指令仅需发送一次，后续调用仍为`ai`开头。

4. **其他功能**
- `来点视频`
- 每日新闻（无需触发，每日定时发送）

具体功能见手册https://tsing-you.github.io/qqbot.html
"""