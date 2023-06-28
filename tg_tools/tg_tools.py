import telegram
import asyncio
import os


async def notify_user(title, year, price, race, city, link, photos, add_text=''):
    token = os.environ.get('TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    bot = telegram.Bot(token=token)

    media_group = [telegram.InputMediaPhoto(link) for link in photos]
    caption = f"{add_text}Авто: {title} {year}\nЦiна: ${price}\nПробiг: {race} km\nМiсто: {city}\nПосилання: {link}"
    await bot.send_media_group(chat_id=chat_id, media=media_group, caption=caption)
