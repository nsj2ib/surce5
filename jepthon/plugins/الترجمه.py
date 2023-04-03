from asyncio import sleep
import requests
import json
from jepthon.helpers.functions.functions import translate
from jepthon import jepiq
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import soft_deEmojify


async def gtrans(text, lan):
    try:
        response = translate(text, lang_tgt=lan)
        if response == 400:
            return Flase
    except Exception as er:
        return f"حدث خطأ \n{er}"
    return response

@jepiq.ar_cmd(
    pattern="ترجمة ([\s\S]*)",
    command=("ترجمة", "tools"),
    info={
        "header": "To translate the text to required language.",
        "note": "For langugage codes check [this link](https://bit.ly/2SRQ6WU)",
        "usage": [
            "{tr}tl <language code> ; <text>",
            "{tr}tl <language codes>",
        ],
        "examples": "{tr}tl te ; Catuserbot is one of the popular bot",
    },
)
async def _(event):
    "To translate the text."
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "en"
    elif ";" in input_str:
        lan, text = input_str.split(";")
    else:
        return await edit_delete(
            event, "** قم بالرد على الرسالة للترجمة **", time=5
        )
    text = soft_deEmojify(text.strip())
    lan = lan.strip()
    if len(text) < 2:
        return await edit_delete(event, "قم بكتابة ما تريد ترجمته!")
    try:
        trans = await gtrans(text, lan)
        if not trans:
            return await edit_delete(event, "**تحقق من رمز اللغة !, لا يوجد هكذا لغة**")      
        output_str = f"**تمت الترجمة من ar الى {lan}**\
                \n`{trans}`"
        await edit_or_reply(event, output_str)
    except Exception as exc:
        await edit_delete(event, f"**خطا:**\n`{exc}`", time=5)
