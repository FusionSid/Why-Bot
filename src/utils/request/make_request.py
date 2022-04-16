import aiohttp

async def get_json(url, data=None):
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


async def post_json(url, data=None):
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


async def get_image(url, data=None):
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


async def post_get_image(url, data=None):
    """
    This function makes a get request to a url and returns the image

    Args:
        url (str) : The url to make a request to
        data (Dict, optional) : This is a dictionary of any extra params to send the request

    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, data=data) as resp:
            response = await resp.read()

    return response
