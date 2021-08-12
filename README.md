# aiocse
An asynchronous wrapper for the [Google Custom Search JSON API](https://developers.google.com/custom-search) written in Python. 
This is basically a copy of [async-cse](https://github.com/souranild/async-cse) with some modifications.

<img alt="google" src="https://i.imgur.com/xpGmyuq.png" align="right">

## Features
- 100% asynchronous (non-blocking)
- Toggle safe-search on/off
- Image search
- Total results 
- Max results
- Query time

## Installation
This library can be installed through PyPi:
```sh
pip install -U aiocse
```

You can also install through GitHub:
```sh
pip install -U git+https://github.com/Daudd/aiocse
```

## Getting Started
An API key is required for aiocse, which you can get one from [here](https://developers.google.com/custom-search/v1/overview). Keep in mind that one key is limited to 100 requests per day, so consider getting more than one key and put them in a list.

![API Key](https://i.imgur.com/pHXFiI8.png)