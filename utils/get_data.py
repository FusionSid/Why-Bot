import aiohttp
import aiofiles


async def get_url_json(url, data=None):
    """
    This function makes a GET request to a url and returns the json

    Args:
        url (str) : The url to make a request to
        data (Dict, optional) : This is a dictionary of any extra params to send the request
    
    Returns:
        Dict : The json response
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=data) as resp:
            try:
                response = await resp.json()
            except Exception as e: 
                print(e)
                response = resp
    return response


async def get_url_image(url, name, data = None):
    """
    This function makes a get request to a url and returns the image and saves
        it to a file in the `tempstorage` directory

    Args:
        url (str) : The url to make a request to
        data (Dict, optional) : This is a dictionary of any extra params to send the request
    
    Returns:
        str : The file path for the image returned
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=data) as resp:
                f = await aiofiles.open(f'./tempstorage/{name}.png', mode='wb')
                await f.write(await resp.read())
                await f.close()
    
    return f'./tempstorage/{name}.png'


async def post_get_json(url, data=None):
    """
    This function makes a POST request to a url and returns the json

    Args:
        url (str) : The url to make a request to
        data (Dict, optional) : This is a dictionary of any extra params to send the request
    
    Returns:
        Dict : The json response
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            try:
                response = await resp.json()
            except Exception as e: 
                print(e)
                response = resp
    return response


async def return_url_image(url, data = None):
    """
    This function makes a get request to a url and returns the image

    Args:
        url (str) : The url to make a request to
        data (Dict, optional) : This is a dictionary of any extra params to send the request
    
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, data=data) as resp:
                response = await resp.read()

    return response