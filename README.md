# Gif-Bot

**Gif-Bot** is a **Telegram bot** written in **Python** using the **Aiogram** library.

It receives GIF with meme and finds information about the origin of that meme using **Bing Search API**, **OpenCV**, **BeautifulSoup**, and **Requests** library.

![IMG_20230329_221636](https://user-images.githubusercontent.com/88056536/228645627-fee0823a-a6ea-4e85-a3aa-69d30e9c43de.jpg)

## How It Works

First, when a user presses the 'start' command the bot sends a greeting message.

When a user sends a GIF with a meme, the bot saves it to disk in the MP4 format, splits it into frames using **OpenCV**, and then saves the non-identical frames to a folder. The similarity between images is checked using the **Scikit-Image** library.

After that, the bot performs a Visual Search and Web Search using the **Bing API** and finds a link to the knowyourmeme.com website - the Internet Meme Database. Then extracts information about the meme's name and origin with **BeautifulSoup** by following this link.

Finally, the bot sends the found information to the user.

## Showcase



https://user-images.githubusercontent.com/88056536/228647590-0b96ea61-64e7-4407-9164-1e895eced3cf.mp4

