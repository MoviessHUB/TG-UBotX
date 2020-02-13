# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# Ported from Watzon's tg_userbot

import asyncio

from telethon.tl.types import MessageEntityMentionName, MessageEntityMention

from userbot import bot
from userbot import GBAN_GROUP
from ..help import add_help_item
from userbot.events import register
from userbot.utils import parse_arguments, get_user_from_event

@register(outgoing=True, pattern=r"^\.fban(\s+[\S\s]+|$)")
async def fedban_all(msg):

    reply_message = await msg.get_reply_message()

    params = msg.pattern_match.group(1) or ""
    args, text = parse_arguments(params, ['reason'])

    if reply_message:
        banid = reply_message.from_id
        banreason = args.get('reason', '[spam]')
    else:
        banreason = args.get('reason', '[fban]')
        if text.isnumeric():
            banid = int(text)
        elif msg.message.entities:
            ent = await bot.get_entity(text)
            if ent: banid = ent.id

    if banid is None:
        return await msg.edit("**No user to ban**")

    failed = dict()
    count = 1

    if GBAN_GROUP:
        async with bot.conversation(GBAN_GROUP) as conv:
            await conv.send_message(f"/fban {banid} {banreason}")
            resp = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
            await msg.reply("**Fbanned!**")
            # Sleep to avoid a floodwait.
            # Prevents floodwait if user is a fedadmin on too many feds
            await asyncio.sleep(0.2)


add_help_item(
    "fban",
    "Admin",
    "Give FedBan through userbot",
    """
.fban [ID/username] [reason]
.unfban [ID/username] [reason]
    """
)
