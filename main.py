from controller import Controller
import asyncio
import traceback

c = Controller()
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(c.run())
except:
    loop.run_until_complete(c.throw_error(traceback.format_exc()))
    traceback.print_exc()