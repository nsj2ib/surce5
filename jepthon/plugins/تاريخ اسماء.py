# Copyright (C) 2021 JepThon TEAM
# FILES WRITTEN BY  @lMl10l
import asyncio

from telethon.errors.rpcerrorlist import YouBlockedUserError

from jepthon import jepiq

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import get_user_from_event, sanga_seperator
from ..helpers.utils import _format

plugin_category = "utils"


@jepiq.ar_cmd(
    pattern="تاريخ(معرفات)?(?: |$)(.*)",
    command=("تاريخ", plugin_category),
    info={
        "header": "To get name history of the user.",
        "flags": {
            "u": "That is sgu to get username history.",
        },
        "usage": [
            "{tr}sg <username/userid/reply>",
            "{tr}sgu <username/userid/reply>",
        ],
        "examples": "{tr}sg @missrose_bot",
    },
)
async def _(event):  #   : @lMl10l
    "To get name/username history."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        await edit_delete( #ترجمه فريق الجوكر على التيلكرام
            event,
            "𓆝︙  يـجب الـرد على الشخـص او كتـابة معـرفه مع الأمـر لأظـهار تواريـخ اسمـه",
        )
    user, rank = await get_user_from_event(event, secondgroup=True)
    if not user:
        return
    uid = user.id
    chat = "@SangMataInfo_bot"
    catevent = await edit_or_reply(event, "𓆝︙ انتظر قليلا..")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message(f"/search_id {uid}")
        except YouBlockedUserError:
            await edit_delete(catevent, "الغـي حـظر @Sangmatainfo_bot وحـاول مـجددا")
        responses = []
        while True:
            try:
                response = await conv.get_response(timeout=2)
            except asyncio.TimeoutError:
                break
            responses.append(response.text)
        await event.client.send_read_acknowledge(conv.chat_id)
    if not responses:
        await edit_delete(catevent, "𓆝︙ لم يتم ايجاد اي نتيجـة")
    if "No records found" in responses:
        await edit_delete(catevent, "𓆝︙ هـذا المـستخدم لـيس لديـه اي سـجل")
    names, usernames = await sanga_seperator(responses)
    cmd = event.pattern_match.group(1)
    jasem = None
    check = usernames if cmd == "معرفات" else names
    for i in check:
        if jasem:
            await event.reply(i, parse_mode=_format.parse_pre)
        else:#ترجمه فريق الجوكر على التيلكرام
            jasem = True
            await catevent.edit(i, parse_mode=_format.parse_pre)
