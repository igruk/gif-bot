# Gif-Bot

**Gif-Bot** is a **Telegram bot** written in **Python** using the **Aiogram** library.

It receives GIFs with memes and finds information about the origin of that meme using **OpenCV**, **BeautifulSoup**, and web scraping.

![IMG_20230329_221636](https://user-images.githubusercontent.com/88056536/228645627-fee0823a-a6ea-4e85-a3aa-69d30e9c43de.jpg)

## How It Works

First, when a user presses the /start command the bot saves the user's information in the **MongoDB** database and writes a greeting message.

When a user sends a GIF with a meme, the bot saves it to disk in the MP4 format, breaks it down into frames using **OpenCV**, and then saves the non-identical frames to a folder. The similarity between frames is checked using **PIL** and **ImageHash** library.

The app then goes through the saved images in the folder and, using the **Requests** library, performs a Google search for image. After receiving the search results page, the app uses web scraping to find the meme's name.

With the meme's name, the app forms a new query to Google by adding the word "knowyourmeme". After receiving the search results page, the app uses web scraping to find the link to knowyourmeme.com website - the Internet Meme Database. By following this link, the app extracts information about the meme's name and origin with **BeautifulSoup**.

After that bot will send to the user name and origin of the meme.

If the meme is not found on the knowyourmeme.com website, the bot will send to the user name of the meme that Google provided.

## Showcase



https://user-images.githubusercontent.com/88056536/228647590-0b96ea61-64e7-4407-9164-1e895eced3cf.mp4

