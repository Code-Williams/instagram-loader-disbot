import instaloader, os, discord, asyncio, json, lzma

client = discord.Client()
insta = instaloader.Instaloader()

@client.event
async def on_ready():
    print(f"{client.user} is now online")

@client.event
async def on_message(message):
    if message.author.bot:
        print("------------------------------")
        # await message.delete()
        username = message.content.split(" ")[0].lower()

        try:
            insta.download_profile(username, profile_pic_only=True)
        except:
            embed = discord.Embed(description=f"<@{message.author.id}> User not found")
            messageSent = await message.channel.send(embed=embed)
            await asyncio.sleep(5)
            await messageSent.delete()
            return;

        filename = ""
        profileDir = os.listdir(username)
        for file in profileDir:
            if file.endswith(".xz"):
                filename = file

        with lzma.open(f"{username}/{filename}") as f:
            json_bytes = f.read()
            stri = json_bytes.decode('utf-8')
            data = json.loads(stri)

        e = discord.Embed(color=0xff0000, description=f"**Instagram <@{message.author.id}>**: [{username}](https://www.instagram.com/{username})")
        e.set_image(url=data["node"]["profile_pic_url_hd"])
        e.add_field(name="Followers", value=data["node"]["edge_followed_by"]["count"])
        e.add_field(name="Following", value=data["node"]["edge_follow"]["count"])
        await message.channel.send(embed=e)

        for i in os.listdir(f"{username}"):
            os.remove(os.path.join(f"{username}", i))

        os.rmdir(username)
        print("------------------------------")

client.run("BOT_TOKEN")
