from srca.configs import addCommand

@addCommand(['id','ichat','idchat','idc','idg','idgp'])
async def start(_,m):
    await m.reply_photo(
        photo='https://imgur.com/p0G9YqD.png',
        caption=f'''<b>・𝘾𝙏 𝘾𝙃𝙆| ID Info
- - - - - - - - - - - - - - -
<a href="https://t.me/">＄</a> » User ID: <code>{m.from_user.id}</code>
<a href="https://t.me/">＄</a> » Chat ID: <code>{m.chat.id}</code>
- - - - - - - - - - - - - - -</b>'''
    )