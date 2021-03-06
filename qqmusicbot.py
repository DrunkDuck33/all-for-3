from bot import Bot

import logging
import zlib
import json
import code

class QQMusicBot(Bot):
    headers = {}
    data = None

    def __init__(self) -> None:
        self.logger = logging.getLogger(__class__.__name__)
        super().__init__()
        with open("qmusic.json") as f:
            self.headers = json.load(f)
        with open("request_body", "rb") as f:
            self.data = f.read()

    def decode_octetstream(self, data: bytes):
        if data[:5] == b"\x00\x00\x00\x00\x00":
            return json.loads(zlib.decompress(data[:5]))
        return json.loads(zlib.decompress(data))

    async def get_new_post(self):
        url = "https://u.y.qq.com/cgi-bin/musics.fcg"
        qmusic_info = self.decode_octetstream(await self.bot_post_raw(url=url, header=self.headers, data=self.data))
        try:
            new_dynamic = qmusic_info["QMHomePageHeaderCgi249"]["data"]["TabDetail"]["MomentTab"]["List"][0]["v_feed"][0]["v_cell"][1]["text"]
            idx = new_dynamic["v_topic"][0]["start_pos"]
            dynamic_text = new_dynamic["content2"][:idx] + new_dynamic["v_topic"][0]["text"] + new_dynamic["content2"][idx:]
        except:
            self.logger.info("Cannot get qmusic info")
            return {}
        return {
            "qmusic_dynamic": dynamic_text
        }
