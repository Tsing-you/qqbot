from ncatbot.plugin import BasePlugin, CompatibleEnrollment
from ncatbot.core.message import GroupMessage, PrivateMessage
from ncatbot.core.element import MessageChain, Image
import httpx
import re
from urllib.parse import unquote, urlencode

bot = CompatibleEnrollment


class ImageSearchPlugin(BasePlugin):
    name = "ImageSearchPlugin"
    version = "1.0.0"

    async def on_load(self):
        self.register_user_func(
            name="search_image",
            handler=self.handle_search,
            raw_message_filter=r"^搜图\b",
            permission_raise=True,
        )

    async def handle_search(self, msg):
        base_params = {
            "r18": 0,
            "num": 1,
            "tag": [],
            "size": ["regular"],
            "excludeAI": "false",
            "uid": [],
            "keyword": None,
            "dateAfter": None,
            "dateBefore": None,
        }

        # 参数解析逻辑
        param_str = msg.raw_message.lstrip("搜图").strip()
        args_queue = param_str.split()
        current_key = None
        parse_errors = []

        while args_queue:
            item = args_queue.pop(0)

            # 识别参数名（必须是base_params的键或新字母组合）
            if item in base_params or (re.match(r'^[a-zA-Z]+$', item) and len(item) <= 10):
                if current_key:  # 前一个参数缺少值
                    parse_errors.append(f"参数 {current_key} 缺少值")
                current_key = item
            else:
                # 处理带引号的值
                if item.startswith('"'):
                    while args_queue and not item.endswith('"'):
                        item += " " + args_queue.pop(0)
                    item = item.strip('"')

                if current_key:
                    self._update_param(base_params, current_key, item, parse_errors)
                    current_key = None
                else:
                    parse_errors.append(f"未识别的参数值: {item}")

        # 错误处理
        if parse_errors:
            await msg.reply("参数解析错误：\n" + "\n".join(parse_errors))
            return
        if current_key:
            await msg.reply(f"参数 {current_key} 缺少对应值")
            return

        # 构建请求参数
        query_params = []
        valid_params = {
            "r18",
            "num",
            "tag",
            "size",
            "excludeAI",
            "uid",
            "keyword",
            "dateAfter",
            "dateBefore",
        }

        for k in valid_params:
            v = base_params.get(k)
            if v is None:
                continue
            if isinstance(v, list):
                for item in v:
                    query_params.append((k, str(item)))
            else:
                query_params.append((k, str(v)))

        # 生成URL
        encoded_url = "https://api.lolicon.app/setu/v2?" + urlencode(
            query_params, doseq=True
        )
        print(f"[DEBUG] 请求URL: {encoded_url}")

        # 发送请求
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(encoded_url, timeout=20.0)
                resp.raise_for_status()
                data = resp.json()
            except httpx.HTTPStatusError as e:
                await msg.reply(f"API响应错误：{e.response.status_code}")
                return
            except Exception as e:
                await msg.reply(f"请求失败：{str(e)}")
                return

        # 处理结果
        if data.get("error"):
            await msg.reply(f"API错误：{data['error']}")
            return

        images = []
        target_size = base_params["size"][0] if base_params["size"] else "regular"
        for item in data.get("data", [])[: base_params["num"]]:
            if url := item["urls"].get(target_size):
                images.append(Image(url))

        if images:
            # 修正后的代码
            await msg.reply(rtf=MessageChain(images))
        else:
            await msg.reply("未找到符合要求的图片")

    def _update_param(self, params, key, value, error_list):
        """统一参数更新逻辑"""
        try:
            value = unquote(value)
            if key == "r18":
                params[key] = max(0, min(2, int(value)))
            elif key == "num":
                params[key] = max(1, min(20, int(value)))
            elif key in ["tag", "size", "uid"]:
                params[key].append(value)
            elif key == "excludeAI":
                params[key] = "true" if value.lower() == "true" else "false"
            elif key in ["dateAfter", "dateBefore"]:
                params[key] = int(value)
            elif key == "keyword":
                params[key] = value
            else:
                error_list.append(f"未知参数: {key}")
        except ValueError as e:
            error_list.append(f"参数 {key} 的值不合法: {value}")
        except Exception as e:
            error_list.append(f"处理参数 {key} 时发生错误: {str(e)}")
