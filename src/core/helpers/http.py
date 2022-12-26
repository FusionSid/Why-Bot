from io import BytesIO
from typing import Optional, Any
from urllib.parse import urlencode

import aiohttp


async def get_request(
    url: str,
    data: Optional[dict] = None,
    headers: Optional[dict] = None,
    timeout: Optional[int] = None,
) -> Optional[aiohttp.ClientResponse | str | dict]:
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
    data: Optional[dict] = None,
    body: Optional[Any] = None,
    json: Optional[bool] = True,
    headers: Optional[dict] = None,
    timeout: Optional[int] = None,
) -> Optional[aiohttp.ClientResponse | str | dict]:
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
    data: Optional[dict] = None,
    headers: Optional[dict] = None,
    timeout: Optional[int] = None,
    bytes_io: Optional[bool] = False,
) -> Optional[aiohttp.ClientResponse | bytes | BytesIO]:
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
            if resp.ok is False:
                return None

            if bytes_io:
                response_bytes = BytesIO(await resp.read())
                response_bytes.seek(0)
                return response_bytes

            return await resp.read()


async def post_request_bytes(
    url: str,
    data: Optional[dict] = None,
    body: Optional[Any] = None,
    json: Optional[bool] = True,
    headers: Optional[dict] = None,
    timeout: Optional[int] = None,
    bytes_io: Optional[bool] = False,
) -> Optional[aiohttp.ClientResponse | bytes | BytesIO]:
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
            if resp.ok is False:
                return None

            if bytes_io:
                response_bytes = BytesIO(await resp.read())
                response_bytes.seek(0)
                return response_bytes

            return await resp.read()
