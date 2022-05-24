from controller import Controller
import asyncio

c = Controller()
loop = asyncio.get_event_loop()
loop.run_until_complete(c.run_test())
