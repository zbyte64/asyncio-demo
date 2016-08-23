import aiohttp
from aiohttp import web
import os
from functools import partial
from foaas import fuck as frack
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize


stemmer = EnglishStemmer()

stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']) # remove it if you need punctuation

app = web.Application()

async def philosophical_response_maker(route, action_stem, words):
    available_arguments = list(words)
    available_arguments.remove(action_stem)
    url_parts = route.split('/')
    params = dict()
    for url_part in url_parts:
        if '{' in url_part:
            param = url_part[1:-1]
            value = 'John'
            if available_arguments:
                value = available_arguments.pop(0)
            params[param] = value

    path = route.format(**params)

    headers = {
        'Accept': 'text/plain'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get('https://foaas.com/'+path, headers=headers) as resp:
            foaas_message = await resp.text()
            return foaas_message

actions_by_stemming = dict()
for api_call_name, route in frack.actions.items():
    stemmed_name = stemmer.stem(api_call_name)
    actions_by_stemming[stemmed_name] = partial(philosophical_response_maker, route, stemmed_name)


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
                spoken = msg.data
                #use stemming to get the kernel of a word
                list_of_words = [stemmer.stem(i.lower()) for i in wordpunct_tokenize(spoken) if i.lower() not in stop_words]
                for word in list_of_words:
                    if word in actions_by_stemming:
                        chatty_response = await actions_by_stemming[word](list_of_words)
                        ws.send_str(chatty_response)
                        break
        elif msg.tp == aiohttp.MsgType.error:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws


app.router.add_route('GET', '/chat', chatbot)
assets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
app.router.add_static('/', assets_path)
print(assets_path)

if __name__ == '__main__':
    web.run_app(app)
