import aiocse
import asyncio

async def main():
    # you can also put a list of keys and it will shuffle automatically
    # so when a key is out of requests, it will remove from the list and
    # use the remaining keys for today
    google = aiocse.Client('API_KEY')
    try:
        results = await google.search('nuts', max_results=3, safe_search=False)
    except aiocse.SearchException as e:
        print(f"{e.__class__.__name__}: {e}")
    else:
        for result in results:
            print(result.title)
            print(result.description)
            print(result.url)
            print('-----')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())