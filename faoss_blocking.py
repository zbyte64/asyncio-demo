from aiohttp import web
from foaas import fuck as frack
from functools import partial


#route handlers are just async functions that deal with aiohttp.web objects
async def hello(request):
    return web.Response(body=b"Hello, world")


app = web.Application()
app.router.add_route('GET', '/', hello)


def frack_adaptor(action, request):
    '''
    web.Request => foaas => web.Response 
    '''
    response = getattr(frack, action)(**request.match_info)
    return web.Response(body=response.text.encode('utf8'))

for api_call_name, route in frack.actions.items():
    print('available call:', api_call_name, route)
    app.router.add_route('GET', '/'+route, partial(frack_adaptor, api_call_name))


if __name__ == '__main__':
    web.run_app(app)

