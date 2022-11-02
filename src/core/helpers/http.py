from io import BytesIO
from urllib.parse import urlencode

import aiohttp


async def get_request(
    url: str,
    data: dict = None,
    headers: dict = None,
    timeout: int = None,
    return_resp: bool = False,
):
    """Makes a get request and returns the json or text result"""

    if data is not None:
        url = f"{url}?{urlencode(data)}"

    kwargs = {
        "headers": headers,
    }

    if timeout is not None:
        kwargs["timeout"] = aiohttp.ClientTimeout(total=timeout)

    async with aiohttp.ClientSession(**kwargs) as session:
        async with session.get(url) as resp:
            if return_resp:
                return resp

            if resp.ok is False:
                return None

            try:
                return await resp.json()
            except aiohttp.ContentTypeError:
                try:
                    return await resp.text()
                except aiohttp.ContentTypeError:
                    return None


async def post_request(
    url: str,
    data: dict = None,
    body=None,
    json=True,
    headers: dict = None,
    timeout: int = None,
    return_resp: bool = False,
):
    """Makes a post request and returns the json or text result"""

    if data is not None:
        url = f"{url}?{urlencode(data)}"

    kwargs = {
        "headers": headers,
    }

    if timeout is not None:
        kwargs["timeout"] = aiohttp.ClientTimeout(total=timeout)
    async with aiohttp.ClientSession(**kwargs) as session:
        # decide if to do json=body or data=body in session.post()
        json_or_data = "json" if json is True else "data"
        async with session.post(url, **{json_or_data: body}) as resp:
            if return_resp:
                return resp

            if resp.ok is False:
                return None

            try:
                return await resp.json()
            except aiohttp.ContentTypeError:
                try:
                    return await resp.text()
                except aiohttp.ContentTypeError:
                    return None


async def get_request_bytes(
    url: str,
    data: dict = None,
    headers: dict = None,
    timeout: int = None,
    return_resp: bool = False,
    bytes_io: bool = False,
):
    """Makes a get request and returns the byte result. This is useful for something like a file/image"""

    if data is not None:
        url = f"{url}?{urlencode(data)}"

    kwargs = {
        "headers": headers,
    }

    if timeout is not None:
        kwargs["timeout"] = aiohttp.ClientTimeout(total=timeout)

    async with aiohttp.ClientSession(**kwargs) as session:
        async with session.get(url) as resp:
            if return_resp:
                return resp

            if resp.ok is False:
                return None

            if bytes_io:
                response_bytes = BytesIO(await resp.read())
                response_bytes.seek(0)
                return response_bytes

            return await resp.read()


async def post_request_bytes(
    url: str,
    data: dict = None,
    body=None,
    json=True,
    headers: dict = None,
    timeout: int = None,
    return_resp: bool = False,
    bytes_io: bool = False,
):
    """Makes a post request and returns the byte result. This is useful for something like a file/image"""

    if data is not None:
        url = f"{url}?{urlencode(data)}"

    kwargs = {
        "headers": headers,
    }

    if timeout is not None:
        kwargs["timeout"] = aiohttp.ClientTimeout(total=timeout)

    async with aiohttp.ClientSession(**kwargs) as session:
        # decide if to do json=body or data=body in session.post()
        json_or_data = "json" if json is True else "data"
        async with session.post(url, **{json_or_data: body}) as resp:
            if return_resp:
                return resp

            if resp.ok is False:
                return None

            if bytes_io:
                response_bytes = BytesIO(await resp.read())
                response_bytes.seek(0)
                return response_bytes

            return await resp.read()
