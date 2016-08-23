'''
Serves up a minimal chat bot over websocket.
Responses are from faoss.
'''
import aiohttp
from aiohttp import web
import os

from nltk_to_faoss import respond_to_line


app = web.Application()


async def chatbot(request):
    '''
    web.Request => websocket => foaas
    '''
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.tp == aiohttp.MsgType.text:
            if msg.data == 'close':
                await ws.close()
            else:
                chatty_response = await respond_to_line(msg.data)
                if chatty_response:
                    ws.send_str(chatty_response)
        elif msg.tp == aiohttp.MsgType.error:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws


app.router.add_route('GET', '/chat', chatbot)

assets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
app.router.add_static('/', assets_path)


if __name__ == '__main__':
    web.run_app(app)
