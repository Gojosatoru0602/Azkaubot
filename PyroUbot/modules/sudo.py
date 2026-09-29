import asyncio

from pyrogram.enums import *
from pyrogram.errors import FloodWait
from pyrogram.types import *

from PyroUbot import *

__MODULE__ = "sᴜᴅᴏ"
__HELP__ = """
<blockquote><b>『 sᴜᴅᴏ 』</b>

  <b>➢ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}addsudo [@username/replay pesan]</code> 
   <i>penjelasan:</b>untuk akses user lain agar bisa menjalankan fitur userbot mu</i>
   <b>➢ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}delsudo [@username/replay pesan]</code> 
   <i>penjelasan:</b>untuk delete akses username
  <b>➢ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}listsudo</code>
  penjelasan:untuk melihat list yang sudah di addsudo</i></blockquote>
"""

@PY.UBOT("addsudo")
async def _(client, message):
    msg = await message.reply("⏰ Memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit("❌ Silakan Balas Pesan Pengguna Atau Masukkan Username/User ID.")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")

    sudo_users = await get_list_from_vars(client.me.id, "SUDOERS")
    if user.id in sudo_users:
        return await msg.edit(f"❌ {user.first_name} Sudah Menjadi Pengguna Sudo.")

    try:
        await add_to_vars(client.me.id, "SUDOERS", user.id)
        return await msg.edit(f"🏓 {user.first_name} Berhasil Ditambahkan Sebagai Sudo Users.")
    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")

@PY.UBOT("delsudo|unsudo")
async def _(client, message):
    msg = await message.reply("🏓 Memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit("❌ Silakan Balas Pesan Pengguna Atau Masukkan Username/User ID.")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")

    sudo_users = await get_list_from_vars(client.me.id, "SUDOERS")
    if user.id not in sudo_users:
        return await msg.edit(f"❌ {user.first_name} Bukan Bagian Dari Pengguna Sudo.")

    try:
        await remove_from_vars(client.me.id, "SUDOERS", user.id)
        return await msg.edit(f"🏓 {user.first_name} Berhasil Dihapus Dari Daftar Pengguna Sudo.")
    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")

@PY.UBOT("sudolist|listsudo")
async def _(client, message):
    msg = await message.reply("🏓 Memproses...")
    sudo_users = await get_list_from_vars(client.me.id, "SUDOERS")

    if not sudo_users:
        return await msg.edit("❌ Tidak Ada Pengguna Sudo Ditemukan.")

    sudo_list = []
    for user_id in sudo_users:
        try:
            user = await client.get_users(int(user_id))
            sudo_list.append(f"• [{user.first_name}](tg://user?id={user.id}) | <code>{user.id}</code>")
        except:
            continue

    response = f"🏓 Daftar Pengguna Sudo:\n" + "\n".join(sudo_list)
    return await msg.edit(response)