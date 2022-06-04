import json
import logging
from pprint import pformat

from bilibot import BiliBot
from douban_bot import DoubanBot
from pushdeerbot import PushdeerBot
from qqmusicbot import QQMusicBot
from dynamic import VideoDynamic

class Controller:
    message_queue = []
    last_updates = {}

    def __init__(self) -> None:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(__class__.__name__)
        self.load_last()
        self.bili_bot = BiliBot()
        self.douban_bot = DoubanBot()
        self.pushdeer_bot = PushdeerBot()
        self.qqmusic_bot = QQMusicBot()

    def load_last(self) -> None:
        with open("last_update.json") as f:
            self.last_updates = json.load(f)
        self.logger.info("last_update loaded")
        self.logger.info(pformat(self.last_updates))
    
    async def update_douban(self, test=False) -> None:
        if self.message_queue == []:
            return
        for message in self.message_queue:
            await self.douban_bot.update(message, test)
    
    async def update_pushdeer(self) -> None:
        if self.message_queue == []:
            return
        for message in self.message_queue:
            await self.pushdeer_bot.push_notification(message)

    async def run_test(self) -> None:
        a = await self.bili_bot.get_all_metadata()

    def process_bili_info(self, bili_info):
        if bili_info["bili_name"] != self.last_updates["bili_name"]:
            self.message_queue.append(f"大哥改名啦！\n原：{self.last_updates['bili_name']} \n现：{bili_info['bili_name']}")
            self.last_updates["bili_name"] = bili_info["bili_name"]
        if bili_info["bili_sex"] != self.last_updates["bili_sex"]:
            self.message_queue.append(f"大哥长🎤啦！")
            self.last_updates["bili_sex"] = bili_info["bili_sex"]
        if bili_info["bili_face"] != self.last_updates["bili_face"]:
            self.message_queue.append(f"大哥换头像啦！\n原：http://i0.hdslb.com/bfs/face/{self.last_updates['bili_face']} \n现：http://i0.hdslb.com/bfs/face/{bili_info['bili_face']}")
            self.last_updates["bili_face"] = bili_info["bili_face"]
        if bili_info["bili_sign"] != self.last_updates["bili_sign"]:
            self.message_queue.append(f"大哥改签名啦！\n原：{self.last_updates['bili_sign']} \n现：{bili_info['bili_sign']}")
            self.last_updates["bili_sign"] = bili_info["bili_sign"]
        if bili_info["bili_is_live"] is not None and bili_info["bili_is_live"] != self.last_updates["bili_is_live"]:
            self.message_queue.append(f"大哥上/下播？？")
            self.last_updates["bili_is_live"] = bili_info["bili_is_live"]
        if bili_info["bili_live_title"] is not None and bili_info["bili_live_title"] != self.last_updates["bili_live_title"]:
            self.message_queue.append(f"大哥改直播标题啦！\n原：{self.last_updates['bili_live_title']} \n现：{bili_info['bili_live_title']}")
            self.last_updates["bili_live_title"] = bili_info["bili_live_title"]
        if bili_info["bili_live_cover"] is not None and bili_info["bili_live_cover"] != self.last_updates["bili_live_cover"]:
            self.message_queue.append(f"大哥改直播封面啦！\n原：http://i0.hdslb.com/bfs/live/user_cover/{self.last_updates['bili_live_cover']} \n现：http://i0.hdslb.com/bfs/live/user_cover/{bili_info['bili_live_cover']}")
            self.last_updates["bili_live_cover"] = bili_info["bili_live_cover"]
        if bili_info["bili_top_photo"] is not None and bili_info["bili_top_photo"] != self.last_updates["bili_top_photo"]:
            self.message_queue.append(f"大哥改PC头图啦！\n原：http://i1.hdslb.com/bfs/space/{self.last_updates['bili_top_photo']} \n现：http://i1.hdslb.com/bfs/space/{bili_info['bili_top_photo']}")
            self.last_updates["bili_top_photo"] = bili_info["bili_top_photo"]
        if bili_info["bili_birthday"] != self.last_updates["bili_birthday"]:
            self.message_queue.append(f"大哥改生日啦！\n原：{self.last_updates['bili_birthday']} \n现：{bili_info['bili_birthday']}")
            self.last_updates["bili_birthday"] = bili_info["bili_birthday"]
        if bili_info["bili_followers"] != self.last_updates["bili_followers"]:
            # self.message_queue.append(f"大哥关注/取关人啦！\n原：{self.last_updates['bili_followers']} \n现：{bili_info['bili_followers']}")
            self.logger.info(f"大哥关注/取关人啦！\n原：{self.last_updates['bili_followers']} \n现：{bili_info['bili_followers']}")
            self.last_updates["bili_followers"] = bili_info["bili_followers"]
        if bili_info["bili_last_coined"] != self.last_updates["bili_last_coined"]:
            self.message_queue.append(f"大哥给 {bili_info['bili_last_coined']} 投币乐")
            self.last_updates["bili_last_coined"] = bili_info["bili_last_coined"]
        if bili_info["dynamic"].timestamp > self.last_updates["bili_dynamic_last_update"]:
            if type(bili_info["dynamic"]) is VideoDynamic:
                self.message_queue.append(f"大哥发新视频了！！\n\n" + bili_info["dynamic"].summary)
            else:
                self.message_queue.append(f"大哥发新动态了！！\n\n" + bili_info["dynamic"].summary)
            self.last_updates["bili_dynamic_last_update"] = bili_info["dynamic"].timestamp + 1
        if bili_info["bili_last_watched"] != self.last_updates["bili_last_watched"]:
            self.message_queue.append(f"大哥的新追番！\n" + bili_info["bili_last_watched"])
            self.last_updates["bili_last_watched"] = bili_info["bili_last_watched"]
        if bili_info["bili_app_top_photo"] is not None and bili_info["bili_app_top_photo"] != self.last_updates["bili_app_top_photo"]:
            self.message_queue.append(f"大哥改头图啦！\n原：http://i1.hdslb.com/bfs/space/{self.last_updates['bili_app_top_photo']} \n现：http://i1.hdslb.com/bfs/space/{bili_info['bili_app_top_photo']}")
            self.last_updates["bili_app_top_photo"] = bili_info["bili_app_top_photo"]
        if bili_info["bili_top_reply"] != self.last_updates["bili_top_reply"]:
            if bili_info["bili_top_reply"] != "":
                self.message_queue.append(f"大哥的新置顶，快去找她聊天吧～\n{bili_info['bili_top_reply']}")
            else:
                self.message_queue.append(f"大哥把置顶撤啦，该去忙自己的事了～")
            self.last_updates["bili_top_reply"] = bili_info["bili_top_reply"]

    def process_qqmusic_info(self, qmusic_info):
        new_dynamic = qmusic_info["QMHomePageHeaderCgi249"]["data"]["TabDetail"]["MomentTab"]["List"][0]["v_feed"][0]["v_cell"][1]["text"]
        idx = new_dynamic["v_topic"][0]["start_pos"]
        dynamic_text = new_dynamic["content2"][:idx] + new_dynamic["v_topic"][0]["text"] + new_dynamic["content2"][idx:]
        if dynamic_text != self.last_updates["qmusic_dynamic"]:
            self.message_queue.append("大哥在QQ音乐的新动态！\n\n" + dynamic_text)
            self.last_updates["qmusic_dynamic"] = dynamic_text

    async def run(self) -> None:
        while True:
            bili_info = await self.bili_bot.get_all_metadata()
            if bili_info != {}:
                self.process_bili_info(bili_info)
            qqmusic_info = await self.qqmusic_bot.get_new_post()
            if qqmusic_info != {}:
                self.process_qqmusic_info(qqmusic_info)

            with open('last_update.json', 'w') as f:
                json.dump(self.last_updates, f)
            await self.update_douban()
            await self.update_pushdeer()

            self.message_queue = []