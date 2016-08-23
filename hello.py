from aiohttp import web


#route handlers are just async functions that deal with aiohttp.web objects
async def hello(request):
    return web.Response(body=b"Hello, world")


app = web.Application()
app.router.add_route('GET', '/', hello)


if __name__ == '__main__':
    web.run_app(app)

