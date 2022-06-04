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
        return qmusic_info
