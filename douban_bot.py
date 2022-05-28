import logging
import time
import hmac
import base64
import hashlib
import asyncio

from bot import Bot

topic_template = """嘘，不要去原视频下打扰哦～\n----------\n{}\n----------\n"""

class DoubanBot(Bot):
    header = {
        "User-Agent": "api-client/1 com.douban.frodo/7.15.0(225) Android/28 product/sdk_gphone_x86_64 vendor/Google model/Android SDK built for x86_64 brand/google  rom/android  network/wifi  udid/f8af163f705129375d26d88da5e5b609273d8a6d  platform/mobile nd/1",
        "Authorization": None
    }
    auth = None
    potential_dangerous = ["改名", "签名", "直播标题", "动态", "追番", "BV", "大哥的新置顶，快去找她聊天吧"]
    last_post = -1

    def __init__(self) -> None:
        self.logger = logging.getLogger(__class__.__name__)
        super().__init__()
        self.header["Authorization"] = f"Bearer {self.config['douban_auth']}"
        self.auth = self.config['douban_auth']

    def gen_comment_sig(self, topic_id: int, _ts: int) -> str:
        txt = f'POST&%2Fapi%2Fv2%2Fgroup%2Ftopic%2F{topic_id}%2Fcreate_comment&{self.auth}&{_ts}'
        digest = hmac.new(b'bf7dddc7c9cfe6f7', txt.encode(), hashlib.sha1).digest()
        return base64.b64encode(digest).decode("utf-8").replace("=", "%3D").replace("/", "%2F").replace("+", "%2B")

    def edit_post_sig(self, topic_id: int, _ts: int) -> str:
        txt = f'POST&%2Fapi%2Fv2%2Fgroup%2Ftopic%2F{topic_id}%2Fpost&{self.auth}&{_ts}'
        digest = hmac.new(b'bf7dddc7c9cfe6f7', txt.encode(), hashlib.sha1).digest()
        return base64.b64encode(digest).decode("utf-8").replace("=", "%3D").replace("/", "%2F").replace("+", "%2B")

    def gen_get_topic_sig(self, topic_id: int, _ts: int) -> str:
        txt = f'GET&%2Fapi%2Fv2%2Fgroup%2Ftopic%2F{topic_id}%2Fdraft&{self.auth}&{_ts}'
        digest = hmac.new(b'bf7dddc7c9cfe6f7', txt.encode(), hashlib.sha1).digest()
        return base64.b64encode(digest).decode("utf-8").replace("=", "%3D").replace("/", "%2F").replace("+", "%2B")

    def gen_post_sig(self, gid, _ts) -> str:
        txt = f'POST&%2Fapi%2Fv2%2Fgroup%2F{gid}%2Fpost&{self.auth}&{_ts}'
        digest = hmac.new(b'bf7dddc7c9cfe6f7', txt.encode(), hashlib.sha1).digest()
        return base64.b64encode(digest).decode("utf-8").replace("=", "%3D").replace("/", "%2F").replace("+", "%2B")

    def gen_delete_sig(self, topic_id, _ts) -> str:
        txt = f'POST&%2Fapi%2Fv2%2Fgroup%2Ftopic%2F{topic_id}%2Fdelete&{self.auth}&{_ts}'
        digest = hmac.new(b'bf7dddc7c9cfe6f7', txt.encode(), hashlib.sha1).digest()
        return base64.b64encode(digest).decode("utf-8").replace("=", "%3D").replace("/", "%2F").replace("+", "%2B")

    async def post_comment(self, topic_id: int, text: str, with_time=True, test=False) -> None:
        url = f"https://frodo.douban.com/api/v2/group/topic/{topic_id}/create_comment"
        _ts = int(time.time())
        _sig = self.gen_comment_sig(topic_id, _ts)
        if with_time:
            text = time.strftime("%Y-%m-%d %H:%M\n", time.localtime()) + text
        data = {
            "text": text,
            "apikey": "0dad551ec0f84ed02907ff5c42e8ec70",
            "channel": "DoubanTest",
            "udid": "f8af163f705129375d26d88da5e5b609273d8a6d",
            "os_rom": "android",
            "_sig": _sig,
            "_ts": _ts
        }
        await self.bot_post(url=url, data=data, header=self.header, msg=f"post {repr(text)} @ {topic_id}", test=test)
    
    async def get_topic_content(self, topic_id: int) -> str:
        _ts = int(time.time())
        _sig = self.gen_get_topic_sig(topic_id, _ts)
        url = f"https://frodo.douban.com/api/v2/group/topic/{topic_id}/draft?apikey=0dad551ec0f84ed02907ff5c42e8ec70&channel=DoubanTest&udid=f8af163f705129375d26d88da5e5b609273d8a6d&os_rom=android&_sig={_sig}&_ts={_ts}"
        resp = await self.bot_get(url, self.header)
        if "content" not in resp.keys():
            self.logger.fatal(f"Cannot get content of {topic_id}")
            self.logger.fatal(resp)
            return None
        return resp["content"]

    async def edit_topic(self, topic_id: int, title: str, change_content=False, text: str="", with_time=True, test=False) -> None:
        url = f"https://frodo.douban.com/api/v2/group/topic/{topic_id}/post"
        _ts = int(time.time())
        _sig = self.edit_post_sig(topic_id, _ts)
        if with_time:
            title = title + time.strftime("(更新于%m-%d %H:%M)", time.localtime())
        if not change_content:
            original_content = await self.get_topic_content(topic_id)
            if original_content is None:
                return
            text = original_content
        else:
            text = topic_template.format(time.strftime("%Y-%m-%d %H:%M\n", time.localtime()) + text)
        data = {
            "title": title,
            "content": text,
            "original": 0,
            "apikey": "0dad551ec0f84ed02907ff5c42e8ec70",
            "channel": "DoubanTest",
            "udid": "f8af163f705129375d26d88da5e5b609273d8a6d",
            "os_rom": "android",
            "_sig": _sig,
            "_ts": _ts
        }
        await self.bot_post(url=url, data=data, header=self.header, msg=f"edit {repr(title)} {repr(text)} @ {topic_id}", test=test)

    async def post_topic(self, text, title="TEST", gid=576533):
        if int(time.time()) - self.last_post < 10:
            self.logger.info("Sleep 10 seconds to post")
            await asyncio.sleep(10)
        self.last_post = int(time.time())
        url = f"https://frodo.douban.com/api/v2/group/{gid}/post"
        _ts = int(time.time())
        _sig = self.gen_post_sig(gid, _ts)
        data = {
            "title": title,
            "content": '{"blocks":[{"data":null,"depth":0,"entityRanges":[],"inlineStyleRanges":[],"key":"","text":"' + text + '","type":"unstyled"}],"entityMap":{}}',
            "original": 0,
            "apikey": "0dad551ec0f84ed02907ff5c42e8ec70",
            "channel": "DoubanTest",
            "udid": "f8af163f705129375d26d88da5e5b609273d8a6d",
            "os_rom": "android",
            "_sig": _sig,
            "_ts": _ts
        }
        return await self.bot_post(url=url, data=data, header=self.header, msg=f"check if {repr(text)} is safe")

    async def delete_post(self, topic_id):
        url = f"https://frodo.douban.com/api/v2/group/topic/{topic_id}/delete"
        _ts = int(time.time())
        _sig = self.gen_delete_sig(topic_id, _ts)
        data = {
            "apikey": "0dad551ec0f84ed02907ff5c42e8ec70",
            "channel": "DoubanTest",
            "udid": "f8af163f705129375d26d88da5e5b609273d8a6d",
            "os_rom": "android",
            "_sig": _sig,
            "_ts": _ts
        }
        return await self.bot_post(url=url, data=data, header=self.header, msg=f"delete test post")

    async def is_safe(self, text) -> bool:
        topic_posted = await self.post_topic(text=text, title=str(time.time()))
        if topic_posted == {}:
            return False
        is_private = topic_posted["is_private"]
        time.sleep(1)
        await self.delete_post(topic_id=topic_posted["id"])
        return not is_private

    async def update(self, text:str, test=False) -> None:
        topic_text = text
        for dangerous_word in self.potential_dangerous:
            if dangerous_word in topic_text:
                is_safe = await self.is_safe(topic_text)
                if not is_safe:
                    if "改名" in topic_text:
                        topic_text = "大哥改名了！"
                    elif "签名" in topic_text:
                        topic_text = "大哥改签名了！"
                    elif "直播标题" in topic_text:
                        topic_text = "大哥改直播标题了！"
                    elif "追番" in topic_text:
                        topic_text = "大哥有新追番了！"
                    elif "BV" in topic_text:
                        topic_text = topic_text[:4+10] + " 投币乐"
                    elif "动态" in topic_text:
                        topic_text = "大哥发新动态了！！"
                    elif "大哥的新置顶，快去找她聊天吧":
                        topic_text = "大哥的新置顶，快去找她聊天吧～"
                    else:
                        self.logger.info(topic_text)
                        self.logger.info("This is not included? Check it")
                        topic_text = "Bot好像出了点问题"
                    break
        await self.post_comment(self.config["douban_topic_id"], topic_text, test=test)
        time.sleep(1)
        await self.edit_topic(self.config["douban_topic_id"], "望夫石", test=test, change_content=True, text=topic_text)
        time.sleep(1)