'''
foaas api rebuilt using aiohttp
'''
import aiohttp
from aiohttp import web
from foaas import fuck as frack
from functools import partial


app = web.Application()


async def frack_adaptor(action, request):
    '''
    web.Request => foaas => web.Response
    '''
    async with aiohttp.ClientSession() as session:
        headers = {
            'Accept': 'text/plain'
        }
        async with session.get('https://foaas.com'+request.path, headers=headers) as resp:
            #await will be executed last in the line, use parentheses to do actions on a returned coroutine
            return web.Response(body=(await resp.text()).encode('utf8'))

for api_call_name, route in frack.actions.items():
    print('available call:', api_call_name, route)
    app.router.add_route('GET', '/'+route, partial(frack_adaptor, api_call_name))


if __name__ == '__main__':
    web.run_app(app)
