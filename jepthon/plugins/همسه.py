from telethon import events
import random, re
from jepthon.utils import admin_cmd
import asyncio 

# Wespr File by  @lMl10l
# Copyright (C) 2021 JepThon TEAM
@borg.on(
    admin_cmd(pattern="همسة ?(.*)")
)
async def wspr(event):
    if event.fwd_from:
        return
    jepiqb = event.pattern_match.group(1)
    rrrd7 = "@nnbbot"
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    tap = await bot.inline_query(rrrd7, jepiqb) 
    await tap[0].click(event.chat_id)
    await event.delete()
    
@borg.on(admin_cmd("م27"))
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        await event.edit("𓆜︙ اوامر الهمسه واكس او \n\n⌔︙الامر  • `.همسة`\n⌔︙الاستخدام  • لكتابة همسه سرية لشخص في المجموعه \n\n𓆜︙ الامر • `.الهمسة`\n𓆜︙ استخدامه • لعرض كيفية كتابة همسة سرية\n\n𓆜︙ الامر • `.اكس او `\n 𓆜︙ استخدامه • ففط ارسل الامر لبدء لعبة اكس او\n\n𓆜︙ CH  - @SC_60")
        
@borg.on(admin_cmd("الهمسة"))
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        await event.edit("**𓆜︙ شـرح كيـفية كـتابة همـسة سـرية**\n𓆜︙ اولا اكتب الامر  .همسة  بعدها الرسالة بعدها اكتب معرف الشخص\n𓆜︙ مـثال  :   `.همسة ههلا @SC_60`")
        
@borg.on(
    admin_cmd(
       pattern="اكس او$"
    )
)
# كتابة وتعديل فريق الجوكر  #@lMl10l
async def gamez(event):
    if event.fwd_from:
        return
    jmusername = "@xoBot"
    uunzz = "play"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(jmusername, uunzz)
    await tap[0].click(event.chat_id)
    await event.delete()
