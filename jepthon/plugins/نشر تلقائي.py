from telethon import *
from telethon.tl import functions, types
from telethon.tl.functions.channels import GetParticipantRequest, GetFullChannelRequest
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest

from jepthon import jepiq

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.autopost_sql import add_post, get_all_post, is_post, remove_post
from jepthon.core.logger import logging
from ..sql_helper.globals import gvarstatus
from . import BOTLOG, BOTLOG_CHATID
from . import *

async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_object = await event.client.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            self_user = await event.client.get_me()
            user = self_user.id
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        if isinstance(user, int) or user.startswith("@"):
            user_obj = await event.client.get_entity(user)
            return user_obj
        try:
            user_object = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return user_object

@jepiq.on(admin_cmd(pattern="(نشر_تلقائي|النشر_التلقائي)"))
async def _(event):
    if (event.is_private or event.is_group):
        return await edit_or_reply(event, "**𓆜︙ عـذراً .. النشر التلقائي خـاص بالقنـوات فقـط**")
    jok = event.pattern_match.group(1)
    if not jok:
        return await edit_or_reply(event, "**𓆜︙ عـذراً .. قـم بـ إضـافة معـرف/ايـدي القنـاة الى الامـر اولاً**")
    if jok.startswith("@"):
        joker = jok
    elif jok.startswith("https://t.me/"):
        joker = jok.replace("https://t.me/", "@")
    elif str(jok).startswith("-100"):
        joker = str(jok).replace("-100", "")
    else:
        try:
            joker = int(jok)
        except BaseException:
            return await edit_or_reply(event, "**𓆜︙ عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**✾╎الرجـاء التـأكـد مـن المعـرف/الايـدي**")
    try:
        joker = (await event.client.get_entity(joker)).id
    except BaseException:
        return await event.reply("**𓆜︙ عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**✾╎الرجـاء التـأكـد مـن المعـرف/الايـدي**")
    if is_post(str(joker) , event.chat_id):
        return await edit_or_reply(event, "**𓆜︙ النشـر التلقـائي من القنـاة ** `{jok}` **مفعـل مسبقـاً ✓**")
    add_post(str(joker), event.chat_id)
    await edit_or_reply(event, f"**𓆜︙ تم تفعيـل النشـر التلقـائي من القنـاة ** `{jok}` **بنجـاح ✓**")



@jepiq.on(admin_cmd(pattern="(ايقاف_نشر|ايقاف_النشر)"))
async def _(event):
    if (event.is_private or event.is_group):
        return await edit_or_reply(event, "**𓆜︙ عـذراً .. النشر التلقائي خـاص بالقنـوات فقـط**")
    jok = event.pattern_match.group(1)
    if not jok:
        return await edit_or_reply(event, "**𓆜︙ عـذراً .. قـم بـ إضـافة معـرف/ايـدي القنـاة الى الامـر اولاً**")
    if jok.startswith("@"):
        joker = jok
    elif jok.startswith("https://t.me/"):
        joker = jok.replace("https://t.me/", "@")
    elif str(jok).startswith("-100"):
        joker = str(jok).replace("-100", "")
    else:
        try:
            joker = int(jok)
        except BaseException:
            return await edit_or_reply(event, "**𓆜︙ عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**✾╎الرجـاء التـأكـد مـن المعـرف/الايـدي**")
    try:
        joker = (await event.client.get_entity(joker)).id
    except BaseException:
        return await event.reply("**𓆜︙ عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**✾╎الرجـاء التـأكـد مـن المعـرف/الايـدي**")
    if not is_post(str(joker), event.chat_id):
        return await edit_or_reply(event, "**𓆜︙ تم تعطيـل النشر التلقـائي لهـذه القنـاة هنـا .. بنجـاح ✓**")
    remove_post(str(joker), event.chat_id)
    await edit_or_reply(event, f"**𓆜︙ تم ايقـاف النشـر التلقـائي من** `{jok}`")


@jepiq.ar_cmd(incoming=True, forword=None)
async def _(event):
    if event.is_private:
        return
    chat_id = str(event.chat_id).replace("-100", "")
    channels_set  = get_all_post(chat_id)
    if channels_set == []:
        return
    for chat in channels_set:
        if event.media:
            await event.client.send_file(int(chat), event.media, caption=event.text)
        elif not event.media:
            await jepiq.send_message(int(chat), event.message)
