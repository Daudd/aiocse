"""
MIT License

Copyright (c) 2021 Daud

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import random
import aiohttp
import logging

from urllib.parse import quote
from typing import List, Union

from .result import Result
from .errors import APIError, NoResults, TooManyRequests

log = logging.getLogger(__name__)

class Client:
    """Represents a client used to interact with the API.

    Parameters
    ----------
    api_keys: Union[`str`, `list`]
        Your API key to interact with the Google CSE JSON API. This can be a 
        list and will automatically shuffle between them in case one expired.
    engine_id: Optional[`str`]
        The engine ID to use.
    image_engine_id: Optional[`str`]
        The image engine ID to use.
    session: Optional[`ClientSession`]
        A client session to use.
    """

    def __init__(
        self,
        api_keys: Union[str, list],
        engine_id: str = '015786823554162166929:mywctwj8es4',
        image_engine_id: str = '015786823554162166929:szgrbbrrox0',
        session: aiohttp.ClientSession = None
    ) -> None:
        self.api_keys = api_keys
        self.engine_id = engine_id
        self.image_engine_id = image_engine_id
        self.session = session or aiohttp.ClientSession()

    def __repr__(self) -> str:
        return "<aiocse.search.Search object engine_id={0.engine_id!r}>".format(self)

    async def search(
        self, 
        query: str, 
        *, 
        image_search = False, 
        max_results: int = 10, 
        safe_search: bool = True
    ) -> List[Result]:
        """Searches the API for a given query.
        
        Parameters
        ----------
        query: `str`
            The query to search for.
        image_search: `bool`
            Whether to search for images. Defaults to False.
        max_results: `int`
            The maximum amount of results to return. Defaults to 10.
        safe_search: `bool`
            Whether to return safe content. Defaults to True.

        Raises
        ------
        :exc:`APIError`
            The API returned an error.
        :exc:`NoResults`
            The search query returned no results.
        :exc:`TooManyRequests`
            The API key has ran out of requests.

        Returns
        -------
        List[`Result`]
            A list of the search results.
        """

        search_url = 'https://www.googleapis.com/customsearch/v1?{}'
        shuffle = False
        if isinstance(self.api_keys, list):
            shuffle = True

        while self.api_keys:
            key = self.api_keys if not shuffle else random.choice(self.api_keys)
            if self.session.closed:
                self.session = aiohttp.ClientSession() # make a new session

            params = {
                'key': key,
                'cx': self.image_engine_id if image_search else self.engine_id,
                'q': quote(query),
                'num': max_results,
                'safe': 'active' if safe_search else 'off'
            }
            if image_search:
                search_url += '&searchType=image'

            try:
                async with self.session.get(search_url, params=params) as r:
                    resp = await r.json()
            finally:
                await self.session.close()

            error = resp.get('error')
            if error:
                if error.get('errors')[0].get('domain') == 'usageLimits':
                    # API key has exhausted
                    if shuffle:
                        # remove the exhausted key from the list since we no longer use it today
                        self.api_keys.remove(key)
                        fmt = f"[100 Requests Limit] Exhausted key has been removed from list of keys."
                        log.warning(fmt)
                    else:
                        raise TooManyRequests
                else:
                    raise APIError(', '.join([error['message'] for _ in error['errors']]))
            elif not resp.get('items'):
                raise NoResults # given query returned nothing
            else:
                return Result.to_list(resp, image_search)
        else:
            raise TooManyRequests