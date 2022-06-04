import json
import logging
import aiohttp
import time

class Bot:
    config = None
    logger = None
    session = None
    sleep_interval = 30

    def __init__(self) -> None:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.load_config()

    def load_config(self) -> None:
        with open("config.json") as f:
            self.config = json.load(f)
        self.logger.info("config loaded")

    async def bot_post(self, url: str, data: dict, header: dict, msg: str, test=False) -> dict:
        if test:
            self.logger.info("Test: " + msg)
            return {}
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=data, headers=header, timeout=timeout) as resp:
                if resp.status != 200:
                    self.logger.fatal(await resp.text())
                    self.logger.fatal("cannot " + msg)

                    if "douban" in url and "post" in url:
                        error = await resp.json()
                        if error["msg"] == "need_captcha":
                            self.sleep_interval *= 2
                            self.logger.fatal(f"Now sleep {self.sleep_interval} seconds")
                            time.sleep(self.sleep_interval)
                        if error["msg"] == "forbidden word not allowed":
                            return error
                    return {}
                else:
                    if "douban" in url and "post" in url:
                        self.sleep_interval = 30
                    self.logger.info(msg)
                return await resp.json()

    async def bot_post_raw(self, url, data, header):
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=data, headers=header, timeout=timeout) as resp:
                return await resp.content.read()

    async def bot_get(self, url: str, header: dict={}, test=False) -> dict:
        if test:
            return {}
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=header, timeout=timeout) as resp:
                if resp.status != 200:
                    self.logger.fatal(await resp.text())
                    self.logger.fatal("cannot get" + url)
                    return {}
                else:
                    pass
                return await resp.json()