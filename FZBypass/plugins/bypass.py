from time import time
from re import match
from sys import executable, argv
from os import execl
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
    
<i>I can Bypass Various Shortener Links, Scrape links, and More ... </i>
🛃 | <b>Click on below button to use me</b>''',
        quote=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('♻️ Click Here ♻️', url='https://t.me/+-QfSjbyIV945MjNl'),]
            ])
    )

@Bypass.on_message(command('help'))
async def start_msg(client, message):
    await message.reply(f'''<b>Shortener Supported Sites</b>
adrinolinks.com	❌️
anlinks.in	✅️
bindaaslinks.com	✅️
bit.ly + tinyurl.com + aylm.short.gy	✅️
bringlifes.com	✅️
dalink.in	✅️
disk.yandex.ru + yandex.com	✅️
download.mdiskshortner.link	✅️
dropbox.in	✅️
droplink.co	✅️
dtglinks.in	✅️
du-link.in + dulink.in	✅️
earn.moneykamalo.com	✅️
earn2me.com	✅️
earn4link.in	✅️
ez4short.com	✅️
go.earnl.xyz	⚠️
go.flashlink.in	⚠️
go.indiurl.in.net	⚠️
go.lolshort.tech	✅️
gtlinks.me + gyanilinks.com	✅️
hotfile.io + bayfiles.com + megaupload.nz + letsupload.cc + filechan.org + myfile.is + vshare.is + rapidshare.nu + lolabits.se + openload.cc + share-online.is + upvid.cc️	⚠️
indianshortner.in	✅️
indyshare.net	✅️
kpslink.in	✅️
krownlinks.me	✅️
link.tnlink.in	️✅️
link.tnshort.net	✅️
link.vipurl.in + vipurl.in + count.vipurl.in	✅️
link1s.com	✅️
link4earn.com + link4earn.in	✅️
linkbnao.com	✅️
linkfly.me	✅️
linkpays.in	✅️
linksly.co	✅️
linkvertise.com	✅️
linkyearn.com	✅️
m.easysky.in	❌️
mdisk.pro	✅️
mediafire.com	✅️
moneycase.link	✅️
mplaylink.com	✅️
omnifly.in.net	✅️
onepagelink.in	✅️
ouo.io + ouo.press	✅️
pandaznetwork.com	✅️
pkin.me + go.paisakamalo.in	✅️
powerlinks.site	✅️
rocklinks.net	✅️
rslinks.net	❌️
shareus.in + shareus.io + shrs.link	️❌️
sheralinks.com	✅️
short.tnvalue.in	✅️
short2url.in	✅️
short2url.in	✅️
shortingly.com	️✅️
shrdsk.me	✅️
shrdsk.me	️❌️
shrinke.me	✅️
shrinkforearn.xyz	✅️
shrtco.de + 9qr.de + shiny.link	✅️
sklinks.in + sklinks.tech	✅️
sxslink.com	✅️
tamizhmasters.com	✅️
terabox. + terabox. + nephobox. + 4funbox. + mirrobox. + momerybox. + teraboxapp.	✅️
tglink.in	✅️
tinyfy.in	✅️
try2link.com	✅️
tulinks.one + go.tulinks.online + tulinks.online	✅️
url4earn.in	✅️
urllinkshort.in	✅️
urlsopen.com	✅️
urlspay.in	✅️
v2.kpslink.in	✅️
v2links.com	✅️
viplinks.io	✅️
vplinks.in	✅️
xpshort.com + push.bdnewsx.com + techymozo.com	✅️
ziplinker.net	✅️
More Supported Sites...Updating	️♻️

<b>Scrape Supported Sites</b>
cinevood.* (Page)	✅️
kayoanime.com (Page)	✅️
skymovieshd.*	✅️
toonworld4all.* (Page + Episode)	✅️
ww1.sharespark.cfd	✅️

<b>GDrive Supported Sites</b>
appdrive.club (File + Pack)	✅️
drivefire.co	✅️
filepress.space + filebee.*	✅️
gdflix.cc(File + Pack)	❌️
hubdrive.co (Instant Link)	✅️
katdrive.org (Direct Download)	✅️
new9.gdtot.cfd	✅️''',
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
            bp_link = f"<b>Bypass Error:</b> {result}"
        elif is_excep_link(link):
            bp_link = result
        else:
            bp_link = f"<b>Bypass Link:</b> {result}"
        
        if is_excep_link(link):
            parse_data.append(bp_link + "\n\n━━━━━━━✦✗✦━━━━━━━\n\n")
        else:
            parse_data.append(f'┎ <b>Source Link:</b> {link}\n┖ {bp_link}\n\n━━━━━━━✦✗✦━━━━━━━\n\n')
            
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


@Bypass.on_message(command('log') & user(Config.OWNER_ID))
async def send_logs(client, message):
    await message.reply_document('log.txt', quote=True)


@Bypass.on_message(command('restart') & user(Config.OWNER_ID))
async def restart(client, message):
    restart_message = await message.reply('<i>Restarting...</i>')
    await (await create_subprocess_exec('python3', 'update.py')).wait()
    with open(".restartmsg", "w") as f:
        f.write(f"{restart_message.chat.id}\n{restart_message.id}\n")
    execl(executable, executable, *argv)


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
