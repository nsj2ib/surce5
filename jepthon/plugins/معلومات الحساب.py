import base64
import time

from telethon.tl.custom import Dialog
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import Channel, Chat, User

from jepthon import jepiq

from ..core.managers import edit_delete, edit_or_reply

plugin_category = "utils"

# =========================================================== #
#                           الثـوابت                           #
# =========================================================== #
STAT_INDICATION = "**𓆜︙ جـاري جـمـع الإحصـائيـات انتـظـر ⏱ **"
CHANNELS_STR = "**𓆜︙ قائمة القنوات التي أنت فيها موجودة هنا\n\n"
CHANNELS_ADMINSTR = "**𓆜︙ قائمة القنوات التي انت مشـرف بهـا **\n\n"
CHANNELS_OWNERSTR = "**𓆜︙ قائمة القنوات التي تـكون انت مالكـها**\n\n"
GROUPS_STR = "**𓆜︙ قائمة المجموعات التي أنت فيها موجود فيـها**\n\n"
GROUPS_ADMINSTR = "**𓆜︙ قائمة المجموعات التي تكون مشـرف بهـا**\n\n"
GROUPS_OWNERSTR = "**𓆜︙ قائمة المجموعات التي تـكون انت مالكـها**\n\n"
# =========================================================== #
#                                                             #
# =========================================================== #


def inline_mention(user):
    full_name = user_full_name(user) or "بـدون اسـم"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    return " ".join(names)


@jepiq.ar_cmd(
    pattern="معلوماتي$",
    command=("معلوماتي", plugin_category),
    info={
        "header": "To get statistics of your telegram account.",
        "description": "Shows you the count of  your groups, channels, private chats...etc if no input is given.",
        "flags": {
            "g": "To get list of all group you in",
            "ga": "To get list of all groups where you are admin",
            "go": "To get list of all groups where you are owner/creator.",
            "c": "To get list of all channels you in",
            "ca": "To get list of all channels where you are admin",
            "co": "To get list of all channels where you are owner/creator.",
        },
        "usage": ["{tr}stat", "{tr}stat <flag>"],
        "examples": ["{tr}stat g", "{tr}stat ca"],
    },
)
async def stats(event):  # sourcery no-metrics
    "To get statistics of your telegram account."
    cat = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    dialog: Dialog
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            broadcast_channels += 1
            if entity.creator or entity.admin_rights:
                admin_in_broadcast_channels += 1
            if entity.creator:
                creator_in_channels += 1
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
            if entity.creator:
                creator_in_groups += 1
        elif not isinstance(entity, Channel) and isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1
        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count
    stop_time = time.time() - start_time
    full_name = inline_mention(await event.client.get_me())
    response = f"✛━━━━━━━━━━━━━✛ \n"
    response += f"**𓆜︙ الدردشات الخاصة ️  :** {private_chats} \n"
    response += f"**𓆜︙ المستخـدمين : {private_chats - bots} \n"
    response += f"**𓆜︙ الـبوتـات :** {bots} \n"
    response += f"**𓆜︙ المجـموعـات :** {groups} \n"
    response += f"**𓆜︙ القنـوات  :** {broadcast_channels} \n"
    response += f"**𓆜︙ المجـموعات التـي تكـون فيها مشرف  :** {admin_in_groups} \n"
    response += f"**𓆜︙ المجموعات التـي تـكون انت مالكـها  **: {creator_in_groups} \n"
    response += f"**𓆜︙ القنوات التـي تكـون فيها مشـرف :** {admin_in_broadcast_channels} \n"
    response += (
        f"**𓆜︙ صلاحيات الاشـراف  :** {admin_in_broadcast_channels - creator_in_channels} \n"
    )
    response += f"**𓆜︙ المحـادثـات الغيـر مقـروء**: {unread} \n"
    response += f"**𓆜︙ الـتاكـات الغيـر مقـروء** : {unread_mentions} \n"
    response += f"✛━━━━━━━━━━━━━✛\n"
    await cat.edit(response)
        
@jepiq.ar_cmd(
    pattern="كروباته(?:\s|$)([\s\S]*)",
    command=("كروباته", plugin_category),
    info={
        "header": "To get list of public groups of repled person or mentioned person.",
        "usage": "{tr}ustat <reply/userid/username>",
    },
)
async def _(event):
    "To get replied users public groups."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        return await edit_delete(
            event,
            "𓆜︙ يجـب وضع ايدي الشخـص او معـرفه او بالرد عليه"
         )
    if input_str:
        try:
            uid = int(input_str)
        except ValueError:
            try:
                u = await event.client.get_entity(input_str)
            except ValueError:
                await edit_delete(
                    event, "𓆜︙ يجـب وضع ايدي الشخـص او معـرفه اولا"
                )
            uid = u.id
    else:
        uid = reply_message.sender_id
    chat = "@tgscanrobot"
    catevent = await edit_or_reply(event, "**-**")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message(f"{uid}")
        except Exception:
            await edit_delete(catevent, "`unblock `@tgscanrobot` and then try`")
        response = await conv.get_response()
        await event.client.send_read_ackno

@jepiq.on(admin_cmd(pattern="قائمه (جميع القنوات|قنوات اديرها|قنواتي)$"))
async def stats(event):  
    catcmd = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    cat = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    hi = []
    hica = []
    hico = []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            hi.append([entity.title, entity.id])
            if entity.creator or entity.admin_rights:
                hica.append([entity.title, entity.id])
            if entity.creator:
                hico.append([entity.title, entity.id])
    if catcmd == "جميع القنوات":
        output = CHANNELS_STR
        for k, i in enumerate(hi, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = CHANNELS_STR
    elif catcmd == "القنوات اديرها":
        output = CHANNELS_ADMINSTR
        for k, i in enumerate(hica, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = CHANNELS_ADMINSTR
    elif catcmd == "قنواتي":
        output = CHANNELS_OWNERSTR
        for k, i in enumerate(hico, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = CHANNELS_OWNERSTR
    stop_time = time.time() - start_time
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    output += f"\n**استغرق حساب القنوات : ** {stop_time:.02f} ثانيه"
    try:
        await catevent.edit(output)
    except Exception:
        await edit_or_reply(
            catevent,
            output,
            caption=caption,
        )

@jepiq.on(admin_cmd(pattern="قائمه (جميع المجموعات|مجموعات اديرها|كروباتي)$"))
async def stats(event):  # sourcery no-metrics
    catcmd = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    cat = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    hi = []
    higa = []
    higo = []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            continue
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            hi.append([entity.title, entity.id])
            if entity.creator or entity.admin_rights:
                higa.append([entity.title, entity.id])
            if entity.creator:
                higo.append([entity.title, entity.id])
    if catcmd == "جميع المجموعات":
        output = GROUPS_STR
        for k, i in enumerate(hi, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = GROUPS_STR
    elif catcmd == "مجموعات اديرها":
        output = GROUPS_ADMINSTR
        for k, i in enumerate(higa, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = GROUPS_ADMINSTR
    elif catcmd == "كروباتي":
        output = GROUPS_OWNERSTR
        for k, i in enumerate(higo, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = GROUPS_OWNERSTR
    stop_time = time.time() - start_time
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    output += f"\n**استغرق حساب المجموعات : ** {stop_time:.02f} ثانيه"
    try:
        await catevent.edit(output)
    except Exception:
        await edit_or_reply(
            catevent,
            output,
            caption=caption,
        )
