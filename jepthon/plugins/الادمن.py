# edit ~ @lMl10l
# for ~ @Jepthon

from asyncio import sleep

from telethon import functions
from telethon.errors import (
    BadRequestError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatBannedRights,
    InputChatPhotoEmpty,
    MessageMediaPhoto,
)

from jepthon import jepiq

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type
from ..helpers.utils import _format, get_user_from_event
from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import BOTLOG, BOTLOG_CHATID

# =================== STRINGS ============
PP_TOO_SMOL = "**𓆝︙ الصورة صغيرة جدًا** "
PP_ERROR = "**𓆝︙ فشل أثناء معالجة الصورة** "
NO_ADMIN = "**𓆝︙ أنا لست مشرف هنا!!** "
NO_PERM = "**𓆝︙ ليس لدي أذونات كافية!** "
CHAT_PP_CHANGED = "**𓆝︙ تم تغيير صورة الدردشة بنجاح ✅**"
INVALID_MEDIA = "**𓆝︙ ملحق غير صالح** "

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)
#admin plugin for  jepiq
UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

LOGS = logging.getLogger(__name__)
MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

plugin_category = "aadmin" 
# ================================================


@jepiq.ar_cmd(
    pattern="الصورة( -وضع| -حذف)$",
    command=("الصورة", plugin_category),
    info={
        "𓆝︙ الأسـتخدام": "For changing group display pic or deleting display pic",
        "𓆝︙ الشـرح": "Reply to Image for changing display picture",
        "flags": {
            "-s": "To set group pic",
            "-d": "To delete group pic",
        },
        "𓆝︙ الأمـر": [
            "{tr}الصورة -وضع <reply to image>",
            "{tr}gpic -حذف",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def set_group_photo(event):  # sourcery no-metrics
    "For changing Group dp"
    flag = (event.pattern_match.group(1)).strip()
    if flag == "-s":
        replymsg = await event.get_reply_message()
        photo = None
        if replymsg and replymsg.media:
            if isinstance(replymsg.media, MessageMediaPhoto):
                photo = await event.client.download_media(message=replymsg.photo)
            elif "image" in replymsg.media.document.mime_type.split("/"):
                photo = await event.client.download_file(replymsg.media.document)
            else:
                return await edit_delete(event, INVALID_MEDIA)
        if photo:
            try:
                await event.client(
                    EditPhotoRequest(
                        event.chat_id, await event.client.upload_file(photo)
                    )
                )
                await edit_delete(event, CHAT_PP_CHANGED)
            except PhotoCropSizeSmallError:
                return await edit_delete(event, PP_TOO_SMOL)
            except ImageProcessFailedError:
                return await edit_delete(event, PP_ERROR)
            except Exception as e:
                return await edit_delete(event, f"**خـطأ : **`{str(e)}`")
            process = "updated"
    else:
        try:
            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
        except Exception as e:
            return await edit_delete(event, f"**خـطأ : **`{str(e)}`")
        process = "deleted"
        await edit_delete(event, "**𓆝︙ تـم حذف الـصورة بنـجاح ✅")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#صوره_المجموعة\n"
            f"صورة المجموعه {process} بنجاح "
            f"الدردشه: {event.chat.title}(`{event.chat_id}`)",
        )


@jepiq.ar_cmd(
    pattern="رفع مشرف(?:\s|$)([\s\S]*)",
    command=("رفع مشرف", plugin_category),
    info={
        "الامر": "𓆝︙ لرفع الشخص مشرف مع صلاحيات",
        "الشرح": "𓆝︙ لرفع الشخص مشرف بالمجموعه قم بالرد على الشخص\
            \n𓆝︙ تـحتاج الصلاحـيات لـهذا الأمـر",
        "الاستخدام": [
            "{tr}رفع مشرف <ايدي/معرف/بالرد عليه>",
            "{tr}رفع مشرف <ايدي/معرف/بالرد عليه> ",
        ],
    },
    groups_only=True,
    require_admin=True,
)#admin plugin for  jepiq
async def promote(event):
    "𓆝︙ لـرفع مستـخدم مشـرف في الـكروب"
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "Admin"
    if not user:
        return
    catevent = await edit_or_reply(event, "**يـتم الرفـع**")
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    await catevent.edit("**تم رفعه مشرف بالمجموعه بنجاح ✅**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#الـرفـع\
            \nالـمستخـدم: [{user.first_name}](tg://user?id={user.id})\
            \nالـدردشـة: {event.chat.title} (`{event.chat_id}`)",
        )


@jepiq.ar_cmd(
    pattern="تنزيل الكل(?:\s|$)([\s\S]*)",
    command=("تنزيل الكل", plugin_category),
    info={
        "الامر": "𓆝︙ لتنزيل الشخص كن الاشراف",
        "الشرح": "𓆝︙ يقوم هذا الامر بحذف جميع صلاحيات المشرف\
            \n𓆝︙ ملاحظه :**لازم تكون انت الشخص الي رفعه او تكون مالك المجموعه حتى تنزله**",
        "الاستخدام": [
            "{tr}تك <الايدي/المعرف/بالرد عليه>",
            "{tr}تك <الايدي/المعرف/بالرد عليه>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def demote(event):
    "𓆝︙ لـتنزيـل شـخص من الأشـراف"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "**𓆝︙ يـتم التنزيل من الاشراف**")
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    rank = "admin"
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    await catevent.edit("**𓆝︙ تـم تنزيله من قائمه الادمنيه بنجاح ✅**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#تنزيل_مشرف\
            \nالمعرف: [{user.first_name}](tg://user?id={user.id})\
            \nالدردشه: {event.chat.title}(`{event.chat_id}`)",
        )
@jepiq.ar_cmd(
    pattern="طرد(?:\s|$)([\s\S]*)",
    command=("طرد", plugin_category),
    info={
        "𓆝︙ الأسـتخدام": "لـطرد شـخض من الـكروب",
        "𓆝︙ الشـرح": "لـطرد شخص من المـجموعة يستطيع الأنضـمام مرة اخـرى.\
        \n𓆝︙ تـحتاج الصلاحـيات لـهذا الأمـر.",
        "𓆝︙ الأمـر": [
            "{tr}طرد <الايدي/المعرف/بالرد عليه>",
            "{tr}طرد <الايدي/المعرف/بالرد عليه> <السبب> ",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def endmute(event):
    "لـطرد شـخض من الـكروب"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    if user.id == 5328713035:
        return await edit_delete(event, "**- لا يمڪنني حظر مطـوري دي لك**")
    catevent = await edit_or_reply(event, "𓆝︙ يـتم طـرد الـمستخدم أنتـظر")
    try:
        await event.client.kick_participant(event.chat_id, user.id)
    except Exception as e:
        return await catevent.edit(NO_PERM + f"\n{str(e)}")
    if reason:
        await catevent.edit(
            f"𓆝︙ الـمستخدم [{user.first_name}](tg://user?id={user.id})\n 𓆝︙ تـم طرده بنجاح ✅ \n𓆝︙ السـبب : {reason}"
        )
    else:
        await catevent.edit(f"𓆝︙ الـمستخدم [{user.first_name}](tg://user?id={user.id})\n 𓆝︙ تـم طرده بنجاح ✅ ")
@jepiq.ar_cmd(
    pattern="حظر(?:\s|$)([\s\S]*)",
    command=("حظر", plugin_category),
    info={
        "𓆝︙ الاستخدام": "يقـوم بـحظر شخـص في الـكروب الءي اسـتخدمت فيـه الامر.",
        "𓆝︙ الشرح": "لحـظر شخـص من الكـروب ومـنعه من الأنـضمام مجـددا\
            \n𓆝︙ تـحتاج الصلاحـيات لـهذا الأمـر.",
        "𓆝︙ الامر": [
            "{tr}حظر <الايدي/المعرف/بالرد عليه>",
            "{tr}حظر <الايدي/المعرف/بالرد عليه> <السبب>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _ban_person(event):
    "𓆝︙ لحـظر شخص في كـروب مـعين"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    if user.id == 5328713035:
        return await edit_delete(event, "**- لا يمڪنني حظر مطـوري دي لك**")
    catevent = await edit_or_reply(event, "𓆝︙ تـم حـظره بـنجاح")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await catevent.edit(
            "𓆝︙ ليـس لـدي جـميع الصـلاحيـات لكـن سيـبقى محـظور"
        )
    if reason:
        await catevent.edit(
            f"𓆝︙ المسـتخدم {_format.mentionuser(user.first_name ,user.id)} \n 𓆝︙ تـم حـظره بنـجاح !!\n**⌔︙السبب : **`{reason}`"
        )
    else:
        await catevent.edit(
            f"𓆝︙ المسـتخدم {_format.mentionuser(user.first_name ,user.id)} \n 𓆝︙ تـم حـظره بنـجاح ✅"
        )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"𓆝︙ الحـظر\
                \nالمسـتخدم: [{user.first_name}](tg://user?id={user.id})\
                \nالـدردشـة: {event.chat.title}\
                \nايدي الكروب(`{event.chat_id}`)\
                \nالسبـب : {reason}",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"𓆝︙ الحـظر\
                \nالمسـتخدم: [{user.first_name}](tg://user?id={user.id})\
                \nالـدردشـة: {event.chat.title}\
                \n ايـدي الكـروب: (`{event.chat_id}`)",
            )


@jepiq.ar_cmd(
    pattern="الغاء حظر(?:\s|$)([\s\S]*)",
    command=("الغاء حظر", plugin_category),
    info={
        "𓆝︙ الأسـتخدام": "يقـوم بـالغاء حـظر الشـخص في الـكروب الذي اسـتخدمت فيـه الامر.",
        "𓆝︙ الشرح": "لألـغاء حـظر شخـص من الكـروب والسـماح له من الأنـضمام مجـددا\
            \n𓆝︙ تـحتاج الصلاحـيات لـهذا الأمـر.",
        "𓆝︙ الأمـر": [
            "{tr}الغاء حظر <الايدي/المعرف/بالرد عليه>",
            "{tr}الغاء حظر <الايدي/المعرف/بالرد عليه> <السبب> ",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def nothanos(event):
    "𓆝︙ لألـغاء الـحظر لـشخص في كـروب مـعين"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "𓆝︙ جـار الـغاء الـحظر أنتـظر رجـاءا")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await catevent.edit(
            f"𓆝︙ الـمستخدم {_format.mentionuser(user.first_name ,user.id)}\n 𓆝︙ تـم الـغاء حـظره بنـجاح "
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "𓆝︙ الـغاء الـحظر \n"
                f"الـمستخدم: [{user.first_name}](tg://user?id={user.id})\n"
                f"الـدردشـة: {event.chat.title}(`{event.chat_id}`)",
            )
    except UserIdInvalidError:
        await catevent.edit("𓆝︙ يـبدو أن هذه الـعمليـة تم إلغاؤهـا")
    except Exception as e:
        await catevent.edit(f"**خـطأ :**\n`{e}`")


@jepiq.ar_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))
