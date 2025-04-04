from ncatbot.core import BotClient, GroupMessage, PrivateMessage
from ncatbot.utils.config import config
from ncatbot.utils.logger import get_log
from ncatbot.core.message import GroupMessage
from zhipuai import ZhipuAI
import httpx
import tempfile
import os
import asyncio
from httpx import TimeoutException, RemoteProtocolError
from PIL import Image
import queue
import threading
from ncatbot.core.element import MessageChain, Image
import json

# 初始化配置
config.set_bot_uin("3779759971")
config.set_root("1956831886")
config.set_ws_uri("ws://localhost:3001")
config.set_token("")

bot = BotClient()

if __name__ == "__main__":
    bot.run()
