from time import time
from re import match
from asyncio import create_task, gather, sleep as asleep, create_subprocess_exec
from pyrogram.filters import command, private, user
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from pyrogram.enums import MessageEntityType
from pyrogram.errors import QueryIdInvalid

from FZBypass import Config, Bypass, BOT_START, LOGGER
from FZBypass.core.bypass_checker import direct_link_checker, is_excep_link
from FZBypass.core.bot_utils import chat_and_topics, convert_time
from FZBypass.core.exceptions import DDLException


@Bypass.on_message(command('start'))
async def start_msg(client, message):
    await message.reply(f'''<b>Link Bypass Bot | LiveTeleBots</b>
    
I can Bypass Various Shortener Links, Scrape links, and More
Use /cmd to see all commands list
🛃 | <b>Click on below button to use me</b>''',
        quote=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('♻️ Click Here ♻️', url='https://t.me/+-QfSjbyIV945MjNl'),]
            ])
    )

@Bypass.on_message(command('help'))
async def start_msg(client, message):
    await message.reply(f'''🩸 SUPPORTED SITES LIST
**Last Updated on 05/09/2023**
**__Click on below button to check site, that can be bypassed using this bot__**''',
        quote=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('👋 SUPPORTED SITES LIST 👋', url='https://throwbin.in/ndl1v3'),]
            ])
    )

@Bypass.on_message(command('alive'))
async def start_msg(client, message):
    await message.reply(f'''<b>I am active Bro.. 🥵</b>''',
        quote=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('♻️ Click Here ♻️', url='https://t.me/+-QfSjbyIV945MjNl'),]
            ])
    )

@Bypass.on_message(command('about'))
async def start_msg(client, message):
    await message.reply(f'''<b>🤖 My Name: Link Bypass Bot | LiveTeleBots
🧑 Developer: <a href='https://t.me/bhaiyajihubbot'>Bhaiyaji</a>
📚 Library: <a href='https://docs.pyrogram.org/'>Pyrogram</a>
🗣 Language: <a href='https://www.python.org/download/releases/3.0/'>Pythgon 3</a>
🌐 Database: <a href='https://www.mongodb.com/'>MongoDB</a>
📊 Build Status: v1.0.0 [ Sᴛᴀʙʟᴇ ]</b>''',
        quote=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('♻️ Support Channel ♻️', url='https://t.me/livetelebots'),]
            ])
    )

@Bypass.on_message(command('cmd'))
async def start_msg(client, message):
    await message.reply(f'''🩸 Commands Available
👉 /alive - To check status of bot, if alive or not
👉 /help - To see supported sites list that can be bypassed using our bot
👉 /about - Info of Bot and Contact details of Developer''',
        quote=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('📞 Contact Us! 📞', url='https://t.me/bhaiyajihubbot'),]
            ])
    )

@Bypass.on_message(command(['bypass', 'bp', 'b']) & (user(Config.OWNER_ID) | chat_and_topics))
async def bypass_check(client, message):
    uid = message.from_user.id
    if (reply_to := message.reply_to_message) and (reply_to.text is not None or reply_to.caption is not None):
        txt = reply_to.text or reply_to.caption
        entities = reply_to.entities or reply_to.caption_entities
    elif len(message.command) > 1:
        txt = message.text
        entities = message.entities
    else:
        return await message.reply('<i>No Link Provided!</i>')
    
    wait_msg = await message.reply("<i>Bypassing...</i>")
    start = time()

    link, tlinks, no = '', [], 0
    atasks = []
    for enty in entities:
        if enty.type == MessageEntityType.URL:
            link = txt[enty.offset:(enty.offset+enty.length)]
        elif enty.type == MessageEntityType.TEXT_LINK:
            link = enty.url
            
        if link:
            no += 1
            tlinks.append(link)
            atasks.append(create_task(direct_link_checker(link)))
            link = ''

    completed_tasks = await gather(*atasks, return_exceptions=True)
    
    parse_data = []
    for result, link in zip(completed_tasks, tlinks):
        if isinstance(result, Exception):
            bp_link = f"\n┖ <b>Bypass Error:</b> {result}"
        elif is_excep_link(link):
            bp_link = result
        elif isinstance(result, list):
            bp_link, ui = "", "┖"
            for ind, lplink in reversed(list(enumerate(result, start=1))):
                bp_link = f"\n{ui} <b>{ind}x Bypass Link:</b> {lplink}" + bp_link
                ui = "┠"
        else:
            bp_link = f"\n┖ <b>Bypass Link:</b> {result}"
    
        if is_excep_link(link):
            parse_data.append(f"{bp_link}\n\n━━━━━━━✦✗✦━━━━━━━\n\n")
        else:
            parse_data.append(f'┎ <b>Source Link:</b> {link}{bp_link}\n\n━━━━━━━✦✗✦━━━━━━━\n\n')
            
    end = time()

    if len(parse_data) != 0:
        parse_data[-1] = parse_data[-1] + f"┎ <b>Total Links : {no}</b>\n┠ <b>Results In <code>{convert_time(end - start)}</code></b> !\n┖ <b>By </b>{message.from_user.mention} ( #ID{message.from_user.id} )"
    tg_txt = "━━━━━━━✦✗✦━━━━━━━\n\n"
    for tg_data in parse_data:
        tg_txt += tg_data
        if len(tg_txt) > 4000:
            await wait_msg.edit(tg_txt, disable_web_page_preview=True)
            wait_msg = await message.reply("<i>Fetching...</i>", reply_to_message_id=wait_msg.id)
            tg_txt = ""
            await asleep(2.5)
    
    if tg_txt != "":
        await wait_msg.edit(tg_txt, disable_web_page_preview=True)
    else:
        await wait_msg.delete()


@Bypass.on_message(command('log') & user(Config.OWNER_ID))
async def send_logs(client, message):
    await message.reply_document('log.txt', quote=True)


@Bypass.on_inline_query()
async def inline_query(client, query):
    answers = [] 
    string = query.query.lower()
    if string.startswith("!bp "):
        link = string.strip('!bp ')
        start = time()
        try:
            bp_link = await direct_link_checker(link)
            end = time()
            
            if not is_excep_link(link):
                bp_link = f"┎ <b>Source Link:</b> {link}\n┃\n┖ <b>Bypass Link:</b> {bp_link}"
            answers.append(InlineQueryResultArticle(
                title="✅️ Bypass Link Success !",
                input_message_content=InputTextMessageContent(
                    f'{bp_link}\n\n_________________________\n\n🧭 <b>Took Only <code>{convert_time(end - start)}</code></b>',
                    disable_web_page_preview=True,
                ),
                description=f"Bypass via !bp {link}",
                reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton('Bypass Again', switch_inline_query_current_chat="!bp ")]
                ])
            ))
        except Exception as e:
            bp_link = f"<b>Bypass Error:</b> {e}"
            end = time()

            answers.append(InlineQueryResultArticle(
                title="❌️ Bypass Link Error !",
                input_message_content=InputTextMessageContent(
                    f'┎ <b>Source Link:</b> {link}\n┃\n┖ {bp_link}\n\n_________________________\n\n🧭 <b>Took Only <code>{convert_time(end - start)}</code></b>',
                    disable_web_page_preview=True,
                ),
                description=f"Bypass via !bp {link}",
                reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton('Bypass Again', switch_inline_query_current_chat="!bp ")]
                ])
            ))    
        
    else:
        answers.append(InlineQueryResultArticle(
                title="♻️ Bypass Usage: In Line",
                input_message_content=InputTextMessageContent(
                    '''<b><i>Link Bypass Bot | LiveTeleBots</i></b>
    
    <i>A Powerful Elegant Multi Threaded Bot written in Python... which can Bypass Various Shortener Links, Scrape links, and More ... </i>
    
🎛 <b>Inline Use :</b> !bp [Single Link]''',
                ),
                description="Bypass via !bp [link]",
                reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔅 Our Channel", url="https://t.me/livetelebots"),
                        InlineKeyboardButton('Try Bypass', switch_inline_query_current_chat="!bp ")]
                ])
            ))
    try:
        await query.answer(
            results=answers,
            cache_time=0
        )
    except QueryIdInvalid:
        pass
