import asyncio
import os
import re
from io import BytesIO
from random import choice, randint
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont
from requests import get
from telethon.utils import get_display_name

from jepthon import jepiq

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.utils import get_user_from_event, reply_id
from . import ALIVE_NAME

plugin_category = "extra"

#كـتابة وتعـديل  @lMl10l
# JepThon ™
async def amongus_gen(text: str, clr: int) -> str:
    url = "https://github.com/JepThon-AR/jepiq-Resources/raw/master/Resources/Amongus/"
    font = ImageFont.truetype(
        BytesIO(
            get(
                "https://github.com/JepThon-AR/jepiq-Resources/raw/master/Resources/fonts/bold.ttf"
            ).content
        ),
        60,
    )
    imposter = Image.open(BytesIO(get(f"{url}{clr}.png").content))
    text_ = "\n".join("\n".join(wrap(part, 30)) for part in text.split("\n"))
    w, h = ImageDraw.Draw(Image.new("RGB", (1, 1))).multiline_textsize(
        text_, font, stroke_width=2
    )
    text = Image.new("RGBA", (w + 30, h + 30))
    ImageDraw.Draw(text).multiline_text(
        (15, 15), text_, "#FFF", font, stroke_width=2, stroke_fill="#000"
    )
    w = imposter.width + text.width + 10
    h = max(imposter.height, text.height)
    image = Image.new("RGBA", (w, h))
    image.paste(imposter, (0, h - imposter.height), imposter)
    image.paste(text, (w - text.width, 0), text)
    image.thumbnail((512, 512))
    output = BytesIO()
    output.name = "imposter.webp"
    webp_file = os.path.join(Config.TEMP_DIR, output.name)
    image.save(webp_file, "WebP")
    return webp_file


async def get_imposter_img(text: str) -> str:
    background = get(
        f"https://github.com/JepThon-AR/jepiq-Resources/raw/master/Resources/imposter/impostor{randint(1,22)}.png"
    ).content
    font = get(
        "https://github.com/JepThon-AR/jepiq-Resources/raw/master/Resources/fonts/roboto_regular.ttf"
    ).content
    font = BytesIO(font)
    font = ImageFont.truetype(font, 30)
    image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    w, h = draw.multiline_textsize(text=text, font=font)
    image = Image.open(BytesIO(background))
    x, y = image.size
    draw = ImageDraw.Draw(image)
    draw.multiline_text(
        ((x - w) // 2, (y - h) // 2), text=text, font=font, fill="white", align="center"
    )
    output = BytesIO()
    output.name = "impostor.png"
    webp_file = os.path.join(Config.TEMP_DIR, output.name)
    image.save(webp_file, "png")
    return webp_file

@jepiq.ar_cmd(
    pattern="من القاتل(|بريء) ([\s\S]*)",
    command=("من القاتل", plugin_category),
    info={
        "header": "Find imposter with stickers animation.",
        "description": "Imp for imposter impn for not imposter",
        "usage": ["{tr}imp <name>", "{tr}impn <name>"],
        "examples": ["{tr}imp blabla", "{tr}impn blabla"],
    },
)
async def _(event):
    "Find imposter with stickers animation."
    USERNAME = f"tg://user?id={event.client.uid}"
    name = event.pattern_match.group(2)
    cmd = event.pattern_match.group(1).lower()
    text1 = await edit_or_reply(event, "𓆝︙ هممم اكيـد اكو شـخص مات !!")
    await asyncio.sleep(2)
    await text1.delete()
    stcr1 = await event.client.send_file(
        event.chat_id, "CAADAQADRwADnjOcH98isYD5RJTwAg"
    )
    text2 = await event.reply(
        f"**[{ALIVE_NAME}]({USERNAME}) :** لقـد عـملت اجـتماع هـام"
    )
    await asyncio.sleep(3)
    await stcr1.delete()
    await text2.delete()
    stcr2 = await event.client.send_file(
        event.chat_id, "CAADAQADRgADnjOcH9odHIXtfgmvAg"
    )
    text3 = await event.reply(
        f"**[{ALIVE_NAME}]({USERNAME}) :** نحـن 3 يجـب ان نصوت علـى احـد او نخـسر "
    )
    await asyncio.sleep(3)
    await stcr2.delete()
    await text3.delete()
    stcr3 = await event.client.send_file(
        event.chat_id, "CAADAQADOwADnjOcH77v3Ap51R7gAg"
    )
    text4 = await event.reply(f"**- الاخـرين :** أيــن??? ")
    await asyncio.sleep(2)
    await text4.edit(f"**- الاخـرين :** مــن ?? ")
    await asyncio.sleep(2)
    await text4.edit(
        f"**[{ALIVE_NAME}]({USERNAME}) :** أنـه {name} , لقـد شاهـدت {name}  يستـخدم الفيـنت ,"
    )
    await asyncio.sleep(3)
    await text4.edit(f"**- الاخـرين :**حسـنا .. صـوتوا علـى {name} ")
    await asyncio.sleep(2)
    await stcr3.delete()
    await text4.delete()
    stcr4 = await event.client.send_file(
        event.chat_id, "CAADAQADLwADnjOcH-wxu-ehy6NRAg"
    )
    catevent = await event.reply(f"**𓆝︙  {name} تـم استـبعاده .......**")
    await asyncio.sleep(2)
    await catevent.edit("ඞㅤㅤㅤㅤ ㅤㅤㅤㅤ")
    await asyncio.sleep(0.5)
    await catevent.edit("ㅤඞㅤㅤㅤㅤ ㅤㅤㅤ")
    await asyncio.sleep(0.5)
    await catevent.edit("ㅤㅤ ඞㅤㅤㅤㅤㅤㅤ")
    await asyncio.sleep(0.5)
    await catevent.edit("ㅤㅤㅤ ඞㅤㅤㅤㅤㅤ")
    await asyncio.sleep(0.5)
    await catevent.edit("ㅤㅤㅤㅤ ඞㅤㅤㅤㅤ")
    await asyncio.sleep(0.5)
    await catevent.edit("ㅤㅤㅤㅤㅤ ඞㅤㅤㅤ")
    await asyncio.sleep(0.5)
    await catevent.edit("ㅤㅤㅤㅤㅤㅤ ඞㅤㅤ")
    await asyncio.sleep(0.5)
    await catevent.edit("ㅤㅤㅤㅤㅤㅤㅤ ඞㅤ")
    await asyncio.sleep(0.5)
    await catevent.edit("ㅤㅤㅤㅤㅤㅤㅤㅤ ඞ")
    await asyncio.sleep(0.5)
    await catevent.edit("ㅤㅤㅤㅤㅤㅤㅤㅤ ㅤ")
    await asyncio.sleep(0.2)
    await stcr4.delete()
    if cmd == "":
        await catevent.edit(
            f". 　　　。　　　　•　 　ﾟ　　。 　　.\n .　　　 　　.　　　　　。　　 。　. 　\n\n  . 　　 。   　     ඞ         。 . 　　 • 　　　　•\n\n  ﾟ{name} لقـد كـان الـقاتل.      。　. 　 　       。　.                                        。　. \n                                   　.          。　  　. \n　'        بـاقـي 0 مـن الـقتلة    　 。　.  　　.                。　.        。 　     .          。 　            .               .         .    ,      。\n　　ﾟ　　　.　　.    ,　 　。　 　. 　 .     。"
        )
        await asyncio.sleep(4)
        await catevent.delete()
        await event.client.send_file(event.chat_id, "CAADAQADLQADnjOcH39IqwyR6Q_0Ag")
    elif cmd == "بريء":
        await catevent.edit(
            f". 　　　。　　　　•　 　ﾟ　　。 　　.\n .　　　 　　.　　　　　。　　 。　. 　\n\n  . 　　 。   　     ඞ         。 . 　　 • 　　　　•\n\n  ﾟ{name} لـم يـكن الـقاتل.      。　. 　 　       。　.                                        。　. \n                                   　.          。　  　. \n　'        بـاقـي 1 مـن الـقتلة    　 。　.  　　.                。　.        。 　     .          。 　            .               .         .    ,      。\n　　ﾟ　　　.　　.    ,　 　。　 　. 　 .     。 "
        )
        await asyncio.sleep(4)
        await catevent.delete()
        await event.client.send_file(event.chat_id, "CAADAQADQAADnjOcH-WOkB8DEctJAg")


@jepiq.ar_cmd(
    pattern="القاتل(|بريء) ([\s\S]*)",
    command=("القاتل", plugin_category),
    info={
        "header": "Find imposter with text animation.",
        "description": "timp for imposter timpn for not imposter",
        "usage": ["{tr}timp <name>", "{tr}timpn <name>"],
        "examples": ["{tr}timp blabla", "{tr}timpn blabla"],
    },
)
async def _(event):
    "Find imposter with text animation."
    name = event.pattern_match.group(2)
    cmd = event.pattern_match.group(1).lower()
    catevent = await edit_or_reply(event, f"{name} تـم اخـراجـه.......")
    await asyncio.sleep(2)
    await catevent.edit("ඞㅤㅤㅤㅤ ㅤㅤㅤㅤ")
    await asyncio.sleep(0.8)
    await catevent.edit("ㅤඞㅤㅤㅤㅤ ㅤㅤㅤ")
    await asyncio.sleep(0.8)
    await catevent.edit("ㅤㅤ ඞㅤㅤㅤㅤㅤㅤ")
    await asyncio.sleep(0.8)
    await catevent.edit("ㅤㅤㅤ ඞㅤㅤㅤㅤㅤ")
    await asyncio.sleep(0.8)
    await catevent.edit("ㅤㅤㅤㅤ ඞㅤㅤㅤㅤ")
    await asyncio.sleep(0.8)
    await catevent.edit("ㅤㅤㅤㅤㅤ ඞㅤㅤㅤ")
    await asyncio.sleep(0.8)
    await catevent.edit("ㅤㅤㅤㅤㅤㅤ ඞㅤㅤ")
    await asyncio.sleep(0.8)
    await catevent.edit("ㅤㅤㅤㅤㅤㅤㅤ ඞㅤ")
    await asyncio.sleep(0.8)
    await catevent.edit("ㅤㅤㅤㅤㅤㅤㅤㅤ ඞ")
    await asyncio.sleep(0.8)
    await catevent.edit("ㅤㅤㅤㅤㅤㅤㅤㅤ ㅤ")
    await asyncio.sleep(0.2)
    if cmd == "":
        await catevent.edit(
            f". 　　　。　　　　•　 　ﾟ　　。 　　.\n .　　　 　　.　　　　　。　　 。　. 　\n\n  . 　　 。   　     ඞ         。 . 　　 • 　　　　•\n\n  ﾟ {name} لقـد كـان الـقاتل.      。　. 　 　       。　.                                        。　. \n                                   　.          。　  　. \n　'        بـاقـي 0 مـن الـقتلة    　 。　.  　　.                。　.        。 　     .          。 　            .               .         .    ,      。\n　　ﾟ　　　.　　.    ,　 　。　 　. 　 .     。"
        )
    elif cmd == "بريء":
        await catevent.edit(
            f". 　　　。　　　　•　 　ﾟ　　。 　　.\n .　　　 　　.　　　　　。　　 。　. 　\n\n  . 　　 。   　     ඞ         。 . 　　 • 　　　　•\n\n  ﾟ {name} لـم يـكن الـقاتـل.      。　. 　 　       。　.                                        。　. \n                                   　.          。　  　. \n　'       بـاقـي  1 مـن الـقتلة    　 。　.  　　.                。　.        。 　     .          。 　            .               .         .    ,      。\n　　ﾟ　　　.　　.    ,　 　。　 　. 　 .     。"
        )
