from PyroUbot import *
from PyroUbot.config import OWNER_ID


__MODULE__ = "SUDO"
__HELP__ = """
<blockquote><b>⌬ SUDO CONTROL</b></blockquote>

<blockquote><b>{0}addsudo user_id/username</b>
Menambahkan user ke daftar sudo.
Bisa juga dengan reply pesan pengguna.</blockquote>

<blockquote><b>{0}rmsudo user_id/username</b>
Menghapus user dari daftar sudo.</blockquote>

<blockquote><b>{0}sudolist</b>
Melihat daftar user sudo.</blockquote>
"""


async def _get_target(client, message):
    """Ambil user dari reply atau argumen command."""
    user_id = await extract_user(message)
    if not user_id:
        return None
    try:
        return await client.get_users(user_id)
    except Exception:
        return None


@PY.UBOT("addsudo")
async def _(client, message):
    if not message.from_user or message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Perintah ini hanya bisa digunakan oleh owner.")

    msg = await message.reply_text("⏳ Memproses...")
    user = await _get_target(client, message)

    if not user:
        return await msg.edit(
            f"❌ Pengguna tidak ditemukan.\n\nGunakan: <code>{message.text.split()[0]} user_id/username</code>\n"
            "atau reply pesan pengguna dengan perintah tersebut."
        )

    sudo_users = await get_list_from_vars(bot.me.id, "SUDO_USERS")

    if user.id in sudo_users:
        return await msg.edit(
            f"⚠️ <b>{user.mention}</b> sudah ada di daftar sudo.\n"
            f"ID: <code>{user.id}</code>"
        )

    await add_to_vars(bot.me.id, "SUDO_USERS", user.id)
    return await msg.edit(
        f"✅ <b>{user.mention}</b> berhasil ditambahkan sebagai sudo.\n"
        f"ID: <code>{user.id}</code>"
    )


@PY.UBOT("rmsudo")
async def _(client, message):
    if not message.from_user or message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Perintah ini hanya bisa digunakan oleh owner.")

    msg = await message.reply_text("⏳ Memproses...")
    user = await _get_target(client, message)

    if not user:
        return await msg.edit(
            f"❌ Pengguna tidak ditemukan.\n\nGunakan: <code>{message.text.split()[0]} user_id/username</code>\n"
            "atau reply pesan pengguna dengan perintah tersebut."
        )

    sudo_users = await get_list_from_vars(bot.me.id, "SUDO_USERS")

    if user.id not in sudo_users:
        return await msg.edit(
            f"⚠️ <b>{user.mention}</b> tidak ada di daftar sudo.\n"
            f"ID: <code>{user.id}</code>"
        )

    await remove_from_vars(bot.me.id, "SUDO_USERS", user.id)
    return await msg.edit(
        f"✅ <b>{user.mention}</b> berhasil dihapus dari daftar sudo.\n"
        f"ID: <code>{user.id}</code>"
    )


@PY.UBOT("sudolist")
async def _(client, message):
    if not message.from_user or message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Perintah ini hanya bisa digunakan oleh owner.")

    msg = await message.reply_text("⏳ Mengambil daftar sudo...")
    sudo_users = await get_list_from_vars(bot.me.id, "SUDO_USERS")

    if not sudo_users:
        return await msg.edit("📋 <b>Daftar sudo kosong.</b>")

    lines = []
    for index, user_id in enumerate(sudo_users, 1):
        try:
            user = await client.get_users(int(user_id))
            name = user.first_name or "Unknown"
            if user.last_name:
                name += f" {user.last_name}"
            lines.append(
                f"<b>{index}.</b> <a href=\"tg://user?id={user.id}\">{name}</a> — <code>{user.id}</code>"
            )
        except Exception:
            lines.append(f"<b>{index}.</b> <code>{user_id}</code>")

    return await msg.edit(
        "📋 <b>DAFTAR SUDO</b>\n\n"
        + "\n".join(lines)
        + f"\n\n<b>Total:</b> {len(sudo_users)}"
    )
