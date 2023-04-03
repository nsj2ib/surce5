#========================#
#       JepThon  - lMl10l  #  
# =======================#

from asyncio import sleep

from telethon import events

from jepthon import jepiq
from ..Config import Config


from ..core.managers import edit_or_reply
from ..sql_helper import pmpermit_sql as pmpermit_sql
from ..sql_helper.welcomesql import (
    addwelcome_setting,
    getcurrent_welcome_settings,
    rmwelcome_setting,
)
from . import BOTLOG_CHATID

plugin_category = "utils"

welpriv = Config.PRV_ET or "رحب"
delwelpriv = Config.DELPRV_ET or "حذف رحب"

@jepiq.on(events.ChatAction)
async def _(event):
    cws = getcurrent_welcome_settings(event.chat_id)
    if (
        cws
        and (event.user_joined or event.user_added)
        and not (await event.get_user()).bot
    ):
        a_user = await event.get_user()
        chat = await event.get_chat()
        me = await event.client.get_me()
        title = chat.title or "هـذه الـدردشـه"
        participants = await event.client.get_participants(chat)
        count = len(participants)
        mention = "<a href='tg://user?id={}'>{}</a>".format(
            a_user.id, a_user.first_name
        )
        my_mention = "<a href='tg://user?id={}'>{}</a>".format(me.id, me.first_name)
        first = a_user.first_name
        last = a_user.last_name
        fullname = f"{first} {last}" if last else first
        username = f"@{a_user.username}" if a_user.username else mention
        userid = a_user.id
        my_first = me.first_name
        my_last = me.last_name
        my_fullname = f"{my_first} {my_last}" if my_last else my_first
        my_username = f"@{me.username}" if me.username else my_mention
        file_media = None
        current_saved_welcome_message = None
        if cws:
            if cws.f_mesg_id:
                msg_o = await event.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
                )
                file_media = msg_o.media
                current_saved_welcome_message = msg_o.message
            elif cws.reply:
                current_saved_welcome_message = cws.reply
        if not pmpermit_sql.is_approved(userid):
            pmpermit_sql.approve(userid, "Due to private welcome")
        await sleep(1)
        current_message = await event.client.send_message(
            userid,
            current_saved_welcome_message.format(
                mention=mention,
                title=title,
                count=count,
                first=first,
                last=last,
                fullname=fullname,
                username=username,
                userid=userid,
                my_first=my_first,
                my_last=my_last,
                my_fullname=my_fullname,
                my_username=my_username,
                my_mention=my_mention,
            ),
            file=file_media,
            parse_mode="html",
        )


@jepiq.on(admin_cmd(pattern=f"{welpriv}(?:\s|$)([\s\S]*)"))
async def save_welcome(event):
    "To set private welcome message."
    msg = await event.get_reply_message()
    string = "".join(event.text.split(maxsplit=1)[1:])
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**𓆝︙ التـرحيب الـخاص **\
                \n**𓆝︙ ايدي الدردشـة  :** {event.chat_id}\
                \n**𓆝︙ تم حفـظ الرسالـة الاتيـة كـترحيـب بنجـاح \n** {event.chat.title}, لا تقـم بحـذف هـذه الرسالـة !",
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID, messages=msg, from_peer=event.chat_id, silent=True
            )
            msg_id = msg_o.id
        else:
            await edit_or_reply(
                event,
                "**𓆝︙ حفـظ الوسائـط كجـزء مـن الترحيـب يتطلـب تعييـن فـار BOTLOG_CHATID !**",
            )
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "**𓆝︙ تـم حـفظ الـترحيب الـخاص فـي هـذه الـدردشـة بنـجاح**"
    if addwelcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("saved"))
    rmwelcome_setting(event.chat_id)
    if addwelcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("updated"))
    await edit_or_reply("**𓆝︙ حـدث خطـأ أثنـاء ضبـط رسالـة الترحيـب في هـذه الـدردشـة ️**")


@jepiq.on(admin_cmd(pattern=f"{delwelpriv}(?:\s|$)([\s\S]*)"))
async def del_welcome(event):
    "To turn off private welcome message"
    if rmwelcome_setting(event.chat_id) is True:
        await edit_or_reply(event, "**𓆝︙ تم حـذف الترحيـب الـخاص لهـذه الدردشـة بنجـاح **")
    else:
        await edit_or_reply(event, "**𓆝︙ لـيس لـدي اي رسـالة تـرحيب خـاص هـنا**")


@jepiq.ar_cmd(
    pattern="لستة الترحيب الخاص$",
    command=("لستة الترحيب خاص", plugin_category),
    info={
        "header": "To check current private welcome message in group.",
        "usage": "{tr}listpwel",
    },
)
async def show_welcome(event):
    "To show current private welcome message in group"
    cws = getcurrent_welcome_settings(event.chat_id)
    if not cws:
        await edit_or_reply(event, "**𓆝︙ لـم يتـم حفـظ اي ترحيـب خـاص هـنا **")
        return
    if cws.f_mesg_id:
        msg_o = await event.client.get_messages(
            entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
        )
        await edit_or_reply(
            event, "**𓆝︙ سأقـوم بالترحيـب بالأعضـاء الجـدد بهـذه الرسالـة :**"
        )
        await event.reply(msg_o.message, file=msg_o.media)
    elif cws.reply:
        await edit_or_reply(
            event, "**𓆝︙ سأقـوم بالترحيـب بالأعضـاء الجـدد بهـذه الرسالـة :**"
        )
        await event.reply(cws.reply)
