import aiohttp
import aiofiles


async def get_url_json(url, data=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=data) as resp:
            try:
                response = await resp.json()
            except Exception as e: 
                print(e)
                response = resp
    return response


async def get_url_image(url, name, data = None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=data) as resp:
                f = await aiofiles.open(f'./tempstorage/{name}.png', mode='wb')
                await f.write(await resp.read())
                await f.close()
    
    return f'./tempstorage/{name}.png'


async def post_get_json(url, data=None):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            try:
                response = await resp.json()
            except Exception as e: 
                print(e)
                response = resp
    return response