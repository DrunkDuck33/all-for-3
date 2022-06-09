from bot import Bot
import logging

class PushdeerBot(Bot):
    def __init__(self) -> None:
        self.logger = logging.getLogger(__class__.__name__)
        super().__init__()

    async def push_notification(self, text):
        url = "https://api2.pushdeer.com/message/push"
        data = {
            "pushkey": self.config["pushdeer_api"],
            "text": text,
            "desp": ""
        }
        await self.bot_post(url=url, data=data, header={}, msg=f"push pushdeer: {text}")