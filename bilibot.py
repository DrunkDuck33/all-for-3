from bot import Bot
from dynamic import *
import time

import logging

class BiliBot(Bot):
    def __init__(self) -> None:
        self.logger = logging.getLogger(__class__.__name__)
        super().__init__()
        self.uid = self.config["bili_follow"]
    
    def av_to_bv(self, av):
        key = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        s=[11,10,3,8,4,6]
        xor=177451812
        add=8728348608
        av=(int(str(av).lstrip('av'))^xor)+add
        r=list('BV1  4 1 7  ')
        for a in range(6):
            r[s[a]]=key[av//58**a%58]
        return ''.join(r)
    
    async def get_dynamic(self):
        url = f"https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={self.uid}&need_top=0"
        all_dynamics = await self.bot_get(url=url)
        new_dynamic = None
        forum_uid = 0
        if all_dynamics != {}:
            dynamic = all_dynamics["data"]["cards"][0]
            type = dynamic["desc"]["type"]
            ts = dynamic["desc"]["timestamp"]
            if type == 1:
                card = json.loads(dynamic["card"])
                new_dynamic = RepostDynamic(card)
                new_dynamic.timestamp = ts
            elif type == 2:
                item = json.loads(dynamic["card"])["item"]
                new_dynamic = PicDynamic(item)
                new_dynamic.timestamp = ts
            elif type == 4:
                item = json.loads(dynamic["card"])["item"]
                new_dynamic = TextDynamic(item)
                new_dynamic.timestamp = ts
            elif type == 8:
                card = json.loads(dynamic["card"])
                new_dynamic = VideoDynamic(card)
                new_dynamic.timestamp = ts
            elif type == 64:
                card = json.loads(dynamic["card"])
                new_dynamic = LongDynamic(card)
                new_dynamic.timestamp = ts
            new_dynamic.oid = dynamic["desc"]["dynamic_id"]

            for d in all_dynamics["data"]["cards"]:
                if d["desc"]["type"] == 4:
                    forum_uid = d["desc"]["dynamic_id"]
                    return new_dynamic, forum_uid
        return None, None

    async def get_info(self) -> dict:
        url = f"https://api.bilibili.com/x/space/acc/info?mid={self.uid}"
        return await self.bot_get(url)

    async def get_card(self) -> dict:
        url = f"https://api.bilibili.com/x/web-interface/card?mid={self.uid}&photo=true"
        return await self.bot_get(url)

    async def get_coins(self) -> dict:
        url = f"https://api.bilibili.com/x/space/coin/video?vmid={self.uid}"
        return await self.bot_get(url)

    async def get_watch(self) -> dict:
        url = f"https://api.bilibili.com/x/space/bangumi/follow/list?vmid={self.uid}&type=1&jsonp=jsonp"
        return await self.bot_get(url)

    async def get_app_info(self) -> dict:
        # TODO: Use a gen_sig. Now it's static
        url = f"https://app.bilibili.com/x/v2/space?access_key=7901cdbb776fb3d2033ccd7697422251&actionKey=appkey&ad_extra=B6B03B278B15506D544960C4DAC6A5E27894BE078312E47C953265B09B7ED52180FDC32DBEF914BEEC0852DC41A2FE11B0D306250DEB308945BE76103D2869D72A392356045621ED9C38246F56941B6E28083DF5A1AB351C89AED721F958BD3B13CE7D4323C204689960CBEEA47C0097FEB6D825650F6523EECC593BF3A9E2C600184B385BAF5A7A8AA491810D9C65CAD5F9EC0C9183023692E45BED2C66DB4D491394C724F3F72F77C7DE74C7E8DA34876641D0CC5F20509A43DABD5793290B608D23DDD2F9B2C26C5F8057A44CDFF302EC8E585EC327059CAD03735370C5AB1A47CE00EA29199A18581B9C4E4A5E90486EFBDE4E42841D4AF6C1688B02B64E1D8E4DEFD987DDA25C475646FB4E10E86489FED9BEDFFBE8EC92CB8F8C84FB6D45AA24F0D493378F9657414B34A12FCA6F5B07286BA04377CB22BFA05D352BF070D270BF13F80018724559C76EB4734B28B5D5157AC41E7892BD1C6324CABC83BB0F1612A5343D8B577DE85C148FFCD46900071ED7C8515AC18042C941163978CE001EDAFDFEC8D06ABDE71A88F76871591B996690F71BDA142203FFC6CB7EC4F2D9C1354629D73CFEBB7AF532F3AF37B6AF8D89FF614E346B78D816DBA9592953D800C3C942032374589C07965E879D80AD6C543C1D87EEA892EF24025CA869CF5D964CB42CA7CE3AFE3C281BF71E22D1DF80C92C109857082CDCD29BB7BBA4E48679B77559C400AF6DE8B1726AB37B8DED0159E744D18C08123819020563778ABB6448B208721E9A57866D2A1EBB84D519C1FFA37745AF1EAA77509DF3EE7C2D18A4690E5D991370BF9D02400DDC7F8FBC91030748635BAED1F4189AF13BA13077A131FDCAE0B55412F9C6C65D3FF51111E0FA73D55B5DACE8347D3E7C6BF4D8180E498D9C53610AE08F11ED18A94C9BC1F892349EAD3AEA7A814E0AEB51A1F5CEF199B116E4419863BBD73CC1851BEB6B0A264DA6753F537D178CB23B3F8EAA6C75E71E6CA4A3E776A1C6CD1C31B855AC65880BBAA4BEE33515631707FC0D7FEAB59A13CF99F66E8A08444E1ABCE3D32BE7E597348E3A223E0851AC0B0CC4399A13B267BC4B87B316C1FBEBD486CA3E0B58C04DB94F8119B492A9DD0D491A137CDC6002BF7CDE713C9AEF906B7BFCCDE414A304FA3DE4E37CE489A4F988A4C4C71BB03DE175DA75F1D1B99EF6740F595481A424511E2E5EC43B8546975A34042B238AAB1ACF056CEABF3E6BCD1BFD21DB208DA0C041B6566A5D0D5B30C2EC84F4D34EE1371A2CC3D8268BADAD881142DC613FE84584B0CD4C9F659EC3302867E648BB5B434D237B040EE147F94944A62AED0972ECDCEE0A55348C2A1EEE356FA86D32F964B5561870F47BF768F7811F5F540AFC37C43234BD4C14C33E93F97187A60678C7A8C7FE15A3F31586EDF80BA5A29DA80001AD4E86FEC9EEE6E872&appkey=27eb53fc9058f8c3&build=67300100&c_locale=zh-Hans_CN&device=phone&disable_rcmd=0&fnval=976&fnver=0&force_host=2&fourk=1&from_view_aid=&local_time=-7&mobi_app=iphone&platform=ios&player_net=1&qn=116&s_locale=zh-Hans_CN&sign=407c6a9eaaf4e0bc7a8b91849e20db5f&statistics=%7B%22appId%22%3A1%2C%22version%22%3A%226.73.0%22%2C%22abtest%22%3A%22%22%2C%22platform%22%3A1%7D&ts=1653192978&vmid=33605910"
        return await self.bot_get(url)

    async def get_top_reply(self, oid) -> str:
        url = f"https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next=0&type=17&oid={oid}&mode=3&plat=1&_=1653341080430"
        return await self.bot_get(url)

    async def get_all_metadata(self) -> dict:
        try:
            dynamic, forum_oid = await self.get_dynamic()
        except:
            self.logger.fatal("Cannot get dynamic")
            return {}
        time.sleep(1)
        try:
            info = await self.get_info()
        except:
            self.logger.fatal("Cannot get info")
            return {}
        time.sleep(1)
        try:
            replies = await self.get_top_reply(662016827293958168)
        except:
            self.logger.fatal("Cannot get replies")
            return {}
        time.sleep(1)
        try:
            app_info = await self.get_app_info()
        except:
            self.logger.fatal("Cannot get app_info")
            return {}
        time.sleep(1)
        try:
            if app_info["data"]["season"]["item"] == []:
                # Occasionally this happens
                self.logger.info("Season is empty")
                return {}
            result = {
                "bili_name":                app_info["data"]["card"]["name"],
                "bili_sex":                 app_info["data"]["card"]["sex"],
                "bili_face":                app_info["data"]["card"]["face"].split("face/")[1],
                "bili_sign":                app_info["data"]["card"]["sign"],
                "bili_is_live":             app_info["data"]["live"]["liveStatus"],
                "bili_live_title":          app_info["data"]["live"]["title"],
                "bili_live_cover":          app_info["data"]["live"]["cover"],
                # This is pc top photo
                "bili_top_photo":           info["data"]["top_photo"].split("space/")[1],
                "bili_birthday":            info["data"]["birthday"],
                "bili_followers":           app_info["data"]["card"]["attention"],
                "bili_last_coined":         self.av_to_bv(app_info["data"]["coin_archive"]["item"][0]["param"]) + " " + app_info["data"]["coin_archive"]["item"][0]["title"],
                "bili_last_watched":        app_info["data"]["season"]["item"][0]["title"],
                "dynamic":                  dynamic,
                # This is mobile top photo
                "bili_app_top_photo":       app_info["data"]["images"]["imgUrl"].split("space/")[1],
                "bili_forum_oid":           forum_oid if forum_oid != 0 else 662016827293958168,
                "bili_top_reply":           replies["data"]["top_replies"][0]["content"]["message"] if replies["data"]["top_replies"] is not None else ""
            }
        except Exception as e:
            self.logger.info(info)
            self.logger.info(dynamic.summary)
            self.logger.info(app_info)
            self.logger.info(replies)
            self.logger.fatal("Cannot return bili data")
            self.logger.fatal(e)
            return {}
        return result
