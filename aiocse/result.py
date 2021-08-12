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

GOOGLE_ICON = 'https://image.flaticon.com/teams/slug/google.jpg'

class Result:
    """Represents a result from the given search query.
    
    Attributes
    ----------
    title: `str`
        The title of the returned result.
    snippet: Optional[`str`]
        The short description of the website, if any.
    url: `str`
        The returned website url.
    image_url: Optional[`str`]
        The preview image of the website, if any.
    total: `str`
        The average total results of the given query.
    time: `str`
        The time used to search the query (in seconds).
    """

    def __init__(self, title, description, url, image_url, total, time) -> None:
        self.title = title
        self.description = description
        self.url = url
        self.image_url = image_url
        self.total = total
        self.time = time

    def __repr__(self) -> str:
        return "<aiocse.result.Result object title={0.title!r} description={0.description!r} " \
               "url={0.url!r} image_url={0.image_url!r}>".format(self)

    @classmethod
    def to_list(cls, data, img):
        """Converts a dict to Result object."""

        results = []
        total = data['searchInformation']['formattedTotalResults']
        time = data['searchInformation']['formattedSearchTime']
        for item in data['items']:
            title = item.get('title')
            desc = item.get('snippet')

            if img:
                image_url = item['link']
                try:
                    url = item['image']['contextLink']
                except KeyError:
                    url = image_url
            else:
                url = item['link']
                i = item.get('pagemap')
                if not i:
                    image_url = GOOGLE_ICON
                else:
                    img = i.get('cse_image')
                    if not i:
                        image_url = GOOGLE_ICON
                    else:
                        try:
                            image_url = img[0]['src']
                            if image_url.startswith('x-raw-image'):
                                image_url = i['cse_thumbnail'][0]['src']
                        except TypeError:
                            image_url = GOOGLE_ICON

            results.append(cls(title, desc, url, image_url, total, time))
        return results