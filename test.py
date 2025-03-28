from ncatbot.core import BotClient, GroupMessage, PrivateMessage
from ncatbot.utils.config import config
from ncatbot.utils.logger import get_log
from ncatbot.core.message import GroupMessage
from zhipuai import ZhipuAI
import httpx
import tempfile
import os
from httpx import TimeoutException, RemoteProtocolError
from PIL import Image


_log = get_log()

config.set_bot_uin("3779759971")  # 设置 bot qq 号 (必填)
config.set_root("1956831886")  # 设置 bot 超级管理员账号 (建议填写)
config.set_ws_uri("ws://localhost:3001")  # 设置 napcat websocket server 地址
config.set_token("")  # 设置 token (napcat 服务器的 token)

bot = BotClient()

@bot.group_event()
async def on_group_message(msg: GroupMessage):
    allowed_groups = [561960789, 2167033211, 561476390]
    
    if msg.group_id not in allowed_groups:
        return
    
    # 解析指令和参数
    parts = msg.raw_message.split(maxsplit=1)
    if not parts or parts[0] not in ["冲一发", "冲两发", "冲三发"]:
        return
    
    # 设置r18级别
    command = parts[0]
    r18_level = 0
    if command == "冲一发":
        r18_level = 0
    elif command == "冲两发":
        r18_level = 2
    elif command == "冲三发":
        r18_level = 1
    
    # 处理关键词参数
    keywords = []
    if len(parts) > 1:
        keywords = parts[1].split()
    
    # 构建请求URL
    base_url = f"https://image.anosu.top/pixiv/direct?r18={r18_level}"
    if keywords:
        keyword_param = "|".join(keywords)
        base_url += f"&keyword={keyword_param}"
    
    retries = 3
    
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=60) as client:
                # 使用动态构建的URL
                response = await client.get(base_url)
                # ... 保持原有图片处理逻辑不变 ...



                response.raise_for_status()
                
                if not response.headers["Content-Type"].startswith("image/"):
                    raise ValueError("非图片内容")
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
                    async for chunk in response.aiter_bytes():
                        f.write(chunk)
                    temp_path = f.name
                    
                    # 压缩图片
                    img = Image.open(temp_path)
                    # max_size = (800, 800)
                    # img = img.resize(max_size, Image.LANCZOS)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    img.save(temp_path, "JPEG", optimize=True, quality=70)
                
                await bot.api.post_group_file(
                    group_id=msg.group_id,
                    image=temp_path
                )
                os.remove(temp_path)
                break
                
        except (TimeoutException, RemoteProtocolError, httpx.HTTPStatusError) as e:
            _log.error(f"尝试 {attempt+1}/{retries} 失败: {str(e)}")
        except Exception as e:
            _log.error(f"未知错误: {str(e)}")
            break
    else:
        await bot.api.post_group_msg(
            group_id=msg.group_id,
            text="图片发送失败，请稍后再试"
        )


@bot.private_event()
async def on_private_message(msg: PrivateMessage):
    _log.info(msg)
    if msg.raw_message == "测试":
        await bot.api.post_private_msg(msg.user_id, text="NcatBot 测试成功喵~")


if __name__ == "__main__":
    bot.run(reload=False)
