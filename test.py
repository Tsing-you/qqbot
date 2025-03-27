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

# @bot.group_event()
# async def on_group_message(msg:GroupMessage):
#     if  msg.raw_message == "你好":
#         await bot.api.post_group_msg(msg.group_id, text="你好呀，有什么需要我帮忙的吗？")


@bot.group_event()
async def on_group_message(msg: GroupMessage):
    allowed_groups = [561960789, 2167033211, 561476390]
    
    if msg.group_id not in allowed_groups:
        return
    
    r18_level = 0
    if msg.raw_message in ["冲一发", "冲两发", "冲三发"]:
        if msg.raw_message == "冲一发":
            r18_level = 0
        elif msg.raw_message == "冲两发":
            r18_level = 2
        elif msg.raw_message == "冲三发":
            r18_level = 1
    else:
        return
    
    url = f"https://image.anosu.top/pixiv/direct?r18={r18_level}"
    retries = 3
    
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=60) as client:
                response = await client.get(url)
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

# @bot.group_event()
# async def on_group_message(msg: GroupMessage):
#     allowed_groups = [561960789, 2167033211, 561476390]
    
#     if msg.group_id not in allowed_groups:
#         return  # 仅处理允许的群组
    
#     r18_level = 0  # 默认值
    
#     # 根据指令设置r18参数
#     if msg.raw_message in ["冲一发", "冲两发", "冲三发"]:
#         if msg.raw_message == "冲一发":
#             r18_level = 0
#         elif msg.raw_message == "冲两发":
#             r18_level = 2
#         elif msg.raw_message == "冲三发":
#             r18_level = 1
#     else:
#         return  # 不处理其他消息
    
#     url = f"https://image.anosu.top/pixiv/direct?r18={r18_level}"
#     retries = 3
    
#     for attempt in range(retries):
#         try:
#             async with httpx.AsyncClient(follow_redirects=True, timeout=60) as client:
#                 response = await client.get(url)
#                 response.raise_for_status()
                
#                 if not response.headers["Content-Type"].startswith("image/"):
#                     raise ValueError("非图片内容")
                
#                 with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
#                     async for chunk in response.aiter_bytes():
#                         f.write(chunk)
#                     temp_path = f.name
                
#                 # 发送到消息来源的群组
#                 await bot.api.post_group_file(
#                     group_id=msg.group_id,  # 动态获取群组ID
#                     image=temp_path
#                 )
#                 os.remove(temp_path)
#                 break
                
#         except (TimeoutException, RemoteProtocolError, httpx.HTTPStatusError) as e:
#             _log.error(f"尝试 {attempt+1}/{retries} 失败: {str(e)}")
#         except Exception as e:
#             _log.error(f"未知错误: {str(e)}")
#             break
#     else:
#         await bot.api.post_group_msg(
#             group_id=msg.group_id,  # 动态回复错误信息
#             text="图片发送失败，请稍后再试"
#         )




# @bot.group_event()
# async def on_group_message(msg: GroupMessage):
#     group_uin = 561960789
#     r18_level = 0  # 默认值
    
#     # 根据指令设置r18参数
#     if msg.raw_message in ["冲一发", "冲两发", "冲三发"]:
#         if msg.raw_message == "冲一发":
#             r18_level = 0
#         elif msg.raw_message == "冲两发":
#             r18_level = 2
#         elif msg.raw_message == "冲三发":
#             r18_level = 1
#     else:
#         return  # 不处理其他消息
    
#     url = f"https://image.anosu.top/pixiv/direct?r18={r18_level}"
#     retries = 3
    
#     for attempt in range(retries):
#         try:
#             async with httpx.AsyncClient(follow_redirects=True, timeout=60) as client:
#                 response = await client.get(url)
#                 response.raise_for_status()
                
#                 # 检查内容类型
#                 if not response.headers["Content-Type"].startswith("image/"):
#                     raise ValueError("非图片内容")
                
#                 # 保存为临时文件
#                 with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
#                     async for chunk in response.aiter_bytes():
#                         f.write(chunk)
#                     temp_path = f.name
                
#                 # 发送文件
#                 await bot.api.post_group_file(
#                     group_id=group_uin,
#                     image=temp_path
#                 )
#                 os.remove(temp_path)
#                 break  # 成功则跳出循环
                
#             _log.debug(f"成功发送图片: {url}")
            
#         except (TimeoutException, RemoteProtocolError, httpx.HTTPStatusError) as e:
#             _log.error(f"尝试 {attempt+1}/{retries} 失败: {str(e)}")
#         except Exception as e:
#             _log.error(f"未知错误: {str(e)}")
#             break
#     else:
#         await bot.api.post_group_msg(group_id=group_uin, text="图片发送失败，请稍后再试")




# @bot.group_event()
# async def on_group_message(msg: GroupMessage):
#     _log.info(msg)
#     if msg.raw_message == "测试":
#         await msg.reply(text="NcatBot 测试成功喵~")


# # bot = BotClient()


# @bot.group_event()
# async def on_group_message(msg: GroupMessage):
#     # group_uin = 12345678 # 指定群聊的账号
#     # user_uin = 987654321# 指定用户的账号
#     if msg.raw_message == "来一发":
#         await bot.api.post_group_file(
#             image="https://image.anosu.top/pixiv/direct"
#         )  # 文件路径支持本地绝对路径，相对路径，网址以及base64


@bot.private_event()
async def on_private_message(msg: PrivateMessage):
    _log.info(msg)
    if msg.raw_message == "测试":
        await bot.api.post_private_msg(msg.user_id, text="NcatBot 测试成功喵~")


if __name__ == "__main__":
    bot.run(reload=False)
