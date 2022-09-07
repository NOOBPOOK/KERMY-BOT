import nextcord
from nextcord.ui import Button, View 
from nextcord.utils import get
from nextcord.ext import commands
from dotenv import load_dotenv
import wikipedia
import smtplib
import datetime
import webbrowser
import youtube_dl
import humanfriendly
import time
import random
import asyncio
import asyncpraw
import youtube_dl
from youtubesearchpython.__future__ import VideosSearch

reddit = asyncpraw.Reddit(client_id= "rlxZ8ONX4K12gG28bslAQw",
                     client_secret = "SeclhK30B2TG7ndn7V4gRB6yQs5bmg",
                     username = "Advanced_Daikon756",
                     password = "#noobpookveduki1234",
                     user_agent = "scrbot")

intents=nextcord.Intents(messages = True, message_content=True, guilds = True, voice_states = True, members=True)
client = commands.Bot(command_prefix="%", help_command=None, intents=intents)
music = []
queue = []
dur = []
que_time = 0
gameOver = True
   
@client.command(pass_context = True)
async def join(ctx):
    if ctx.voice_client == None:
        if (ctx.author.voice):
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.reply("Bot connected to play music!🎶")
        else:
            await ctx.reply("You're not in a Voice Channel!🎶")
    else:
        await ctx.reply("The Bot is already connected to a Voice Channel!")
            
@client.command(pass_context = True)
async def leave(ctx):
    if ctx.voice_client:
        global music
        global queue
        global dur
        global que_time
        await ctx.voice_client.disconnect()
        await ctx.reply("Disconnected from Voice channel!")
        music = []
        queue = []
        dura = []
        que_time = 0
    else:
        await ctx.reply("The Bot is not connected to any Voice Channel!")
    
@client.command(pass_context = True)
async def play(ctx,* ,arg):
    if ctx.voice_client:
        if ctx.author.voice:
            global music
            global queue
            global dur
            global que_time
            video = VideosSearch(str(arg),limit=1)
            vid = await video.next()
            url =(vid['result'][0]['link'])
            name = (vid['result'][0]['title'])
            dura = (vid['result'][0]['duration'])
            if len(music) != 0:
                music.append(url)
                queue.append(name)
                dur.append(dura)
                x = dura.split(":")
                dt = int(x[0])*60 + int(x[1])
                que_time+=dt
                await ctx.message.delete()
                await ctx.send(f"**{name}** has been added to the queue\n**Expexted time:- **{int(que_time/60)}:{int(que_time%60)}!")
            else:
                music.append(url)
                queue.append(name)
                dur.append(dura)
                x = dura.split(":")
                dt = int(x[0])*60 + int(x[1])
                que_time+=dt
                await qplay(ctx, url)
        else:
            await ctx.reply("You are not connected to Voice Channel!")
    else:
        await ctx.reply(f"The Bot is not connected to any Voice Channel!")

@client.command()
async def q(ctx):
    global queue
    global dur
    global que_time
    if len(queue)>1:
        mins = int(que_time/60)
        sec = int(que_time%60)
        quebed = nextcord.Embed(title = f"MUSIC QUEUE🎶", description=('\n\n'.join(map(str,queue))) ,color=0x3498db)
        quebed.set_thumbnail(url = "https://cdn.pixabay.com/photo/2018/09/17/14/27/headphones-3683983_960_720.jpg")
        quebed.set_footer(text = f"Time for the whole queue {mins}mins {sec}seconds!")
        await ctx.reply(embed = quebed)
    else:
        await ctx.reply("No Queue Exits!")
    
@client.command()
async def qremove(ctx, n:int):
    global music
    global dur
    global queue
    global que_time
    if n<=(len(music)+1) and n !=0:
        await ctx.reply(f"{queue[n-1]} has been removed from the queue!\nQueue Updated!")
        del music[n-1]
        x = dur[n-1].split(":")
        dt = int(x[0])*60 + int(x[1])
        que_time-=dt
        del dur[n-1]
        del queue[n-1]
    else:
        await ctx.reply("Song doesn't exist at this Position!")

async def qplay(ctx,url):
    global music
    global queue
    global dur
    FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format':'bestaudio'}
    vc = ctx.voice_client
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url , download = False)
        try:
            await ctx.message.delete()
        except:
            print("Not Available!")
           
        url2 = info['formats'][0]['url']
        music_bed = nextcord.Embed(title = f"Music World!", description=f"{info['title']}", color=0x3498db)
        music_bed.set_image(url = f"{info['thumbnails'][3]['url']}")
        music_bed.set_thumbnail(url = "https://cdn.pixabay.com/photo/2018/09/17/14/27/headphones-3683983_960_720.jpg")
        music_bed.set_footer(text = f"Length of the song >>> {dur[0]}")
        await ctx.send(embed = music_bed)
        vc.play(await nextcord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS))
        await music_but(ctx)
               
async def music_but(ctx):
    global button1
    global button2
    global mus_but
    global view
    global but1
    global but2
    but1 = 0
    but2 = 0
    button1 = Button(label="Resume", style=nextcord.ButtonStyle.green, emoji="▶️")
    button2 = Button(label="Pause", style=nextcord.ButtonStyle.blurple, emoji="⏸")
    button3 = Button(label="Skip/Next", style=nextcord.ButtonStyle.danger, emoji="⏭️")
    view = View(timeout=500)
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    mus_but = await ctx.send(view = view)
    async def button_callback(interaction):
        global button2
        global mus_but
        global view
        global but2
        global but1
        if but2 == 1:
            button2.disabled = False
        ctx.voice_client.resume()
        button1.disabled = True
        await mus_but.edit(view = view)
        but1 = 1
    button1.callback = button_callback
    async def button_callback(interaction):
        global button1
        global mus_but
        global view
        global but2
        global but1
        if but1 == 1:
            button1.disabled = False
        ctx.voice_client.pause()
        button2.disabled = True
        await mus_but.edit(view = view)
        but2 = 1
    button2.callback = button_callback
    async def button_callback(interaction):
        global button1
        global button2
        global view
        global mus_but
        global music
        global queue
        global dur
        global que_time
        ctx.voice_client.stop()
        button1.disabled = True
        button2.disabled = True
        button3.disabled = True
        await mus_but.edit(view = view)
        del music[0]
        del queue[0]
        x = dur[0].split(":")
        dt = int(x[0])*60 + int(x[1])
        que_time-=dt
        del dur[0]
        try:
            url = music[0]
            await qplay(ctx, url)
        except:
            await ctx.send("Queue Ended 🎧!")
    button3.callback = button_callback
        
@client.event
async def on_ready():
    print("Bot hello just landed on the server!")
    
@client.command()
async def private(ctx):
    myEmbed = nextcord.Embed(title = "🌟 Kermy's Village 🌟", description=f"Hello there In Private! **{ctx.author}**\nHow may I help you?", color=0xffff00)
    myEmbed.set_author(name="KERMY BOT#5109")
    await ctx.author.send(embed=myEmbed)
    
@client.command()
async def wiki(ctx, *, arg):
    mes_1 = await ctx.reply("Searching Google!")
    try:
        results = wikipedia.page(arg)
        url = results.url
        content = results.content
        await mes_1.edit(content=f"According to Kermy, {url}")
    except Exception as e:
        await mes_1.edit(content="Could not get what you were looking for!")
        
@client.command()
async def luckyroles(ctx, give_rol:nextcord.Role):
    user_give = ctx.author
    user_rol = get(user_give.guild.roles, id=983357105417367612)#Admin Role
    user2_rol = get(user_give.guild.roles, id=983357284660957244)#Modeartor role
    if user_rol in user_give.roles or user2_rol in user_give.roles or user_give == await client.fetch_user(763676643356835840):
        giveaway_mem = random.choice(user_give.guild.members)
        try:
            await giveaway_mem.add_roles(give_rol)
            give_embed = nextcord.Embed(title="🌟 Kermy's Village 🌟", description = f"**{giveaway_mem}** \n You have just won the giveaway held by **{ctx.author}**\n You have got the **{give_rol}** !🎆🎊🎉*", color=0xffff00)
            give_embed.set_thumbnail(url = giveaway_mem.display_avatar)
            await ctx.reply(embed=give_embed)
            try:
                await giveaway_mem.send(embed=give_embed)
            except:
                await ctx.author.send("Cannot send message to the user who won the giveaway!")
        except Exception as e:
            print(e)
            await ctx.send("Above mentioned role doesn't exist or either the bot is unable to give the Role due to less permissions!")
    else:
        await ctx.send(f"You don't have the necessary role to perrform a giveaway!\n You should have **{user_rol}** or **{user2_rol}** to perform giveaway in the server!")
        
@client.command()
async def admin(ctx, pas:int , chn_id:int, *, arg):
    if pas == 5109:
        try:
            chn = client.get_channel(chn_id)
            admin_ctx = await ctx.author.send("Sending your message!")
            await chn.send(arg)
            await admin_ctx.edit(content=f"Your message has been sent successfully to this channel {chn.mention}")
        except Exception as e:
            await admin_ctx.edit(content=f"Your message could not be delivered to the channel!\n Here is why {e}")
    else:
        await ctx.send(f"The above password is Wrong {ctx.author.mention}!\nTry again!")

@client.command()
async def addrole(ctx, mem: nextcord.Member, rol: nextcord.Role):
    user_give = ctx.author
    user_rol = get(user_give.guild.roles, id=983357105417367612)#Admin Role
    user2_rol = get(user_give.guild.roles, id=983357284660957244)#Modeartor role
    if user_rol in user_give.roles or user2_rol in user_give.roles or user_give == await client.fetch_user(763676643356835840):
        try:
            await mem.add_roles(rol)
            rol_emb = nextcord.Embed(title="ROLE UPDATED🔃", description=f"**{rol}** has been given to **{mem}**", color = 0x7289da)
            rol_emb.set_thumbnail(url = mem.display_avatar)
            await ctx.reply(embed = rol_emb)
        except:
            await ctx.reply(f"Something Went Wrong❌,\nCannot give {rol} to {mem}!")
    else:
        await ctx.reply(f"You don't have the necessary permissions!\nOnly {user_rol} and {user2_rol} can use this!")

@client.command()
async def remrole(ctx, mem: nextcord.Member, rol: nextcord.Role):
    user_give = ctx.author
    user_rol = get(user_give.guild.roles, id=983357105417367612)#Admin Role
    user2_rol = get(user_give.guild.roles, id=983357284660957244)#Modeartor role
    if user_rol in user_give.roles or user2_rol in user_give.roles or user_give == await client.fetch_user(763676643356835840):
        try:
            await mem.remove_roles(rol)
            rol_emb = nextcord.Embed(title="Role Updated🔃", description=f"**{rol}** has been removed from **{mem}**!", color=0x7289da)
            rol_emb.set_thumbnail(url = mem.display_avatar)
            await ctx.reply(embed = rol_emb)
        except Exception as e:
            print(e)
            await ctx.reply(f"Something Went Wrong❌,\nCannot remove {rol} from {mem}!")
    else:
        await ctx.reply(f"You don't have the necessary permissions!\nOnly {user_rol} and {user2_rol} can use this!")

@client.command()
async def timeout(ctx, mem: nextcord.Member, time:int, *, arg):
    user_give = ctx.author
    user_rol = get(user_give.guild.roles, id=983357105417367612)#Admin Role
    user2_rol = get(user_give.guild.roles, id=983357284660957244)#Modeartor role
    if user_rol in user_give.roles or user2_rol in user_give.roles or user_give == await client.fetch_user(763676643356835840):
        try:
            await mem.edit(timeout = nextcord.utils.utcnow() + datetime.timedelta(seconds=(time*60)), reason=arg)
            time_emb = nextcord.Embed(title="TIMEOUT❌", description=f"**{mem.mention}** is in timeout for **{time}** minute\n**REASON**:*{arg}*", color=0xe74c3c)
            time_emb.set_footer(text = f"{ctx.author} used this command!")
            time_emb.set_thumbnail(url = mem.display_avatar)
            await ctx.reply(embed = time_emb)
        except Exception as e:
            print(e)
            await ctx.reply(f"Cannot timeout {mem}!")
    else:
        await ctx.reply(f"You don't have the necessary permissions!\nOnly {user_rol} and {user2_rol} can use this!")

@client.command()
async def kick(ctx, mem:nextcord.Member, *, arg=None):
    user_give = ctx.author
    user_rol = get(user_give.guild.roles, id=983357105417367612)#Admin Role
    user2_rol = get(user_give.guild.roles, id=983357284660957244)#Modeartor role
    if user_rol in user_give.roles or user2_rol in user_give.roles or user_give == await client.fetch_user(763676643356835840):
        if arg==None:
            arg="Confidential"
        try:
            url = mem.display_avatar
            await mem.kick(reason=arg)
            mem_emb = nextcord.Embed(title="⭐Kermy's Village⭐", description=f"{mem.mention} was kicked out of the server by {ctx.author}\n**REASON**:*{arg}*", color=0xe74c3c)
            mem_emb.set_thumbnail(url = url)
            await ctx.reply(embed = mem_emb)
        except Exception as e:
            print(e)
            await ctx.reply(f"Cannot kick {mem}!")
    else:
        await ctx.reply(f"You don't have the necessary permissions!\nOnly {user_rol} and {user2_rol} can use this!")
       
@client.command()
async def meme(ctx):
    all_subs = []
    subreddit = await reddit.subreddit("memes")
    top_red = subreddit.top("day", limit=50)
    async for top_hot in top_red:
        all_subs.append(top_hot)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    memEmbed = nextcord.Embed(title= name)
    memEmbed.set_thumbnail(url = "https://static-prod.adweek.com/wp-content/uploads/2021/06/Reddit-Avatar-Builder-Hero-1280x680.png")
    memEmbed.set_image(url = url)
    ctx_mem = await ctx.reply(embed = memEmbed)
    await meme_but(ctx,ctx_mem)
        
async def meme_but(ctx,ctx_mem):
    button = Button(label="Another One!", style=nextcord.ButtonStyle.blurple, emoji="🤚")
    view = View(timeout=100)
    view.add_item(button)
    async def button_callback(interaction):
        await mem_rep(ctx,ctx_mem)
    button.callback = button_callback
    await ctx.reply(view = view)
        
async def mem_rep(ctx,ctx_mem):
    all_subs = []
    subreddit = await reddit.subreddit("memes")
    top_red = subreddit.top("day", limit=50)
    async for top_hot in top_red:
        all_subs.append(top_hot)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    memEmbed = nextcord.Embed(title= name)
    memEmbed.set_thumbnail(url = "https://static-prod.adweek.com/wp-content/uploads/2021/06/Reddit-Avatar-Builder-Hero-1280x680.png")
    memEmbed.set_image(url = url)
    await ctx_mem.edit(embed = memEmbed)
            
@client.command()
async def help(ctx):
    help_embed = nextcord.Embed(title = "**🌟 Kermy's Village 🌟**", description = "Here are the various cmds to help you out!", color=0xffff00)
    help_embed.add_field(name="**🤖COMMANDS🤖**", value=f"1.**\%private**: Opens a dm with the user. \n2.**\%wiki [subject]**: Gives Information about the concerned subject. \n3.**\%luckyroles [role_id]**: Makes a giveaway of the mentioned role if the user has suitable permissions.\n4.**\%admin [password] [channel_id] [content]**: Sends the content matter to the described channel through the bot.\n5.**\%addrole [member] [role]**: Adds the concerned role to the member mentioned!.\n6.**\%remrole [member] [role]**: Removes the role from the mentioned member!\n7.**\%meme**:Gives memes from reddit.\n8.**\%join**:Joins the Voice-Channel.\n9.**\%play [music-word]**:Plays the Best Quality Music.\n10.**\%q**:Gives a list of songs in the queue!.\n11.**\%qremove [song no.]**:Removes the song on that place from the queue!.\n12.**\%timeout [member] [time] [reason]**:Timeouts the mentioned member!\n13.**\%kick [member] [reason]**:Kicks the mentioned member!\n14.**\%rpshelp**:Gives information on how to play game!",inline = True)
    help_embed.set_thumbnail(url = ctx.author.display_avatar)
    help_embed.set_author(name = "KERMY BOT#5109")
    await ctx.reply(embed = help_embed)
    
@client.command()
async def rps(ctx, p1:nextcord.Member, p2:nextcord.Member):
    global gameOver 
    if gameOver:
        global rps_p1
        global rps_p2
        global point1
        global point2
        global rps1
        global rps2
        global score_msg
        global rps1_but
        global rps2_but
        gameOver = False
        rps_p1 = p1
        rps_p2 = p2
        point1 = 0
        point2 = 0
        rps1 = ""
        rps2 = ""
        myEmbed = nextcord.Embed(title = "🌟Kermy's Village🌟", description="🎮Rock, Paper, Scissor🎮", color=0xffff00)
        myEmbed.add_field(name="RULES:-" ,value=f"1.Press the button only once.\n2. Do not cry about cheating!\n4. The game is starting in 5 seconds. Maybe 2 by the time you read this!", inline=True)
        myEmbed.set_author(name="KERMY BOT#5109")
        await ctx.reply(embed = myEmbed)
        await asyncio.sleep(5)
        view = player1()
        rps1_but = await ctx.send(f"For {rps_p1.mention}, Choose within 5 seconds!",view=view)
        score_emb = nextcord.Embed(title="ROCK🥌 PAPER🧻 SCISSOR✂", description=f"{rps_p1.mention}(**{point1}**)⚔{rps_p2.mention}(**{point2}**)", color=0x3498db)
        score_emb.set_thumbnail(url=f"{rps_p1.display_avatar}")
        score_emb.add_field(name="What Happened This Time?", value=f"{rps_p1} choose {rps1} and {rps_p2} choose {rps2}!")
        score_msg = await ctx.send(embed = score_emb)
        view = player2()
        rps2_but = await ctx.send(f"For {rps_p2.mention}, Choose within 5 seconds!",view=view)
        await time(ctx)
    else:
        await ctx.reply(f"{rps_p1.mention} is playing with {rps_p2.mention}!\nPlease try again later!")
 
async def time(ctx):
    global gameOver
    if gameOver:
        return
    else:
        await asyncio.sleep(7)
        await match(ctx)
 
class player1(View):
    @nextcord.ui.button(label="Rock", style=nextcord.ButtonStyle.blurple, emoji="🥌", custom_id="stone_rps1")
    async def stone_button_callback(self, button, interaction):
        global rps_p1
        global rps1
        if interaction.user == rps_p1:
            rps1 = "stone"
            buttons = [x for x in self.children]
            for v in buttons:
                v.disabled = True
            await interaction.response.edit_message(view=self)
    
    @nextcord.ui.button(label="Paper", style=nextcord.ButtonStyle.blurple, emoji="🧻", custom_id="paper_rps1")
    async def paper_button_callback(self, button, interaction):
        global rps_p1
        global rps1
        if interaction.user == rps_p1:
            rps1 = "paper"
            buttons = [x for x in self.children]
            for v in buttons:
                v.disabled = True
            await interaction.response.edit_message(view=self)
    
    @nextcord.ui.button(label="Scissor", style=nextcord.ButtonStyle.blurple, emoji="✂", custom_id="scissor_rps1")
    async def scissor_button_callback(self, button, interaction):
        global rps_p1
        global rps1
        if interaction.user == rps_p1:
            rps1 = "scissor"
            buttons = [x for x in self.children]
            for v in buttons:
                v.disabled = True
            await interaction.response.edit_message(view=self)
            
    @nextcord.ui.button(label="Computer Random", style=nextcord.ButtonStyle.danger, emoji="⚠️", custom_id="random_rps1")
    async def random_button_callback(self, button, interaction):
        global rps_p1
        global rps1
        if interaction.user == rps_p1:
            rps = ["stone","paper","scissor"]
            rps1 = random.choice(rps)
            buttons = [x for x in self.children]
            for v in buttons:
                v.disabled = True
            await interaction.response.edit_message(view=self)

class player2(View):
    @nextcord.ui.button(label="Rock", style=nextcord.ButtonStyle.blurple, emoji="🥌", custom_id="stone_rps")
    async def stone_button_callback(self, button, interaction):
        global rps_p2
        global rps2
        if interaction.user == rps_p2:
            rps2 = "stone"
            buttons = [x for x in self.children]
            for v in buttons:
                v.disabled = True
            await interaction.response.edit_message(view=self)
    
    @nextcord.ui.button(label="Paper", style=nextcord.ButtonStyle.blurple, emoji="🧻", custom_id="paper_rps")
    async def paper_button_callback(self, button, interaction):
        global rps_p2
        global rps2
        if interaction.user == rps_p2:
            rps2 = "paper"
            buttons = [x for x in self.children]
            for v in buttons:
                v.disabled = True
            await interaction.response.edit_message(view=self)
    
    @nextcord.ui.button(label="Scissor", style=nextcord.ButtonStyle.blurple, emoji="✂", custom_id="scissor_rps")
    async def scissor_button_callback(self, button, interaction):
        global rps_p2
        global rps2
        if interaction.user == rps_p2:
            rps2 = "scissor"
            buttons = [x for x in self.children]
            for v in buttons:
                v.disabled = True
            await interaction.response.edit_message(view=self)            

    @nextcord.ui.button(label="Computer Random", style=nextcord.ButtonStyle.danger, emoji="⚠️", custom_id="random_rps1")
    async def random_button_callback(self, button, interaction):
        global rps_p2
        global rps2
        if interaction.user == rps_p2:
            rps = ["stone","paper","scissor"]
            rps2 = random.choice(rps)
            buttons = [x for x in self.children]
            for v in buttons:
                v.disabled = True
            await interaction.response.edit_message(view=self)

async def match(ctx):
    global point1
    global point2
    global rps1
    global rps2
    global rps_p1
    global rps_p2
    if rps1 == "stone" and rps2 == "paper":
        point2 +=1
    elif rps1 == "stone" and rps2 == "":
        point1 +=1
    elif rps1 == "paper" and rps2 == "":
        point1 +=1
    elif rps1 == "scissor" and rps2 == "":
        point1 +=1
    elif rps1 == "stone" and rps2 == "scissor":
        point1 +=1
    elif rps1 == "paper" and rps2 == "stone":
        point1 +=1
    elif rps1 == "paper" and rps2 == "scissor":
        point2+=1
    elif rps1 == "scissor" and rps2 == "stone":
        point2 +=1
    elif rps1 == "scissor" and rps2 == "paper":
        point1 +=1
    await pointcount(ctx)
    
async def pointcount(ctx):
    global point1
    global point2
    global rps_p1
    global rps_p2
    global point1
    global point2
    global rps1
    global rps2
    global gameOver
    global rps1_but
    global rps2_but
    global score_msg
    if gameOver==False:
        if point1<5 and point2<5:
            score_emb = nextcord.Embed(title="ROCK🥌 PAPER🧻 SCISSOR✂", description=f"{rps_p1.mention}(**{point1}**)⚔{rps_p2.mention}(**{point2}**)", color=0x3498db)
            score_emb.set_thumbnail(url=f"{rps_p1.display_avatar}")
            score_emb.add_field(name="What Happened This Time?", value=f"{rps_p1.mention}(**{rps1}**)⚔{rps_p2.mention}(**{rps2}**)")
            await score_msg.edit(embed = score_emb)
            view = player1()
            await rps1_but.edit(f"For {rps_p1.mention}, Choose within 5 seconds!",view=view)
            view = player2()
            await rps2_but.edit(f"For {rps_p2.mention}, Choose within 5 seconds!",view=view)
            rps1 = ""
            rps2 = ""
            await asyncio.sleep(2)
            await time(ctx)
        else:
            if point1==5:
                myEmbed = nextcord.Embed(title = "🌟 Kermy's Village 🌟", description=f"{rps_p1.mention} beat the crap out of {rps_p2.mention}", color=0xffff00)
                myEmbed.add_field(name="Points:", value=f"💹{rps_p1.mention}:   {point1} ⚔ {point2}   :{rps_p2.mention}📉", inline=True)
                myEmbed.set_thumbnail(url=f"{rps_p1.display_avatar}")
                myEmbed.set_author(name="KERMY BOT#5109")
                await score_msg.edit(embed=myEmbed)
            else:
                myEmbed = nextcord.Embed(title = "🌟 Kermy's Village 🌟", description=f"{rps_p2.mention} beat the crap out of {rps_p1.mention}", color=0xffff00)
                myEmbed.add_field(name="Points:", value=f"📉{rps_p1.mention}:   {point1} ⚔ {point2}   :{rps_p2.mention}💹", inline=True)
                myEmbed.set_thumbnail(url=f"{rps_p2.display_avatar}")
                myEmbed.set_author(name="KERMY BOT#5109")
                await score_msg.edit(embed=myEmbed)
            gameOver = True
    else:
        return

@client.command()
async def gameover(ctx):
    global rps_p1
    global rps_p2
    global rps1_but
    global rps2_but
    global score_msg
    global gameOver
    gameOver = True
    await rps1_but.delete()
    await rps2_but.delete()
    winner = random.randint(1,2)
    if winner==1:
        win_emb = nextcord.Embed(title="ROCK🥌 PAPER🧻 SCISSOR✂", description=f"{rps_p1.mention} beat the crap out of {rps_p2.mention} through toss!", color=0xffff00)
        win_emb.set_thumbnail(url = rps_p1.display_avatar)
        await ctx.reply(embed = win_emb)
    else:
        win_emb = nextcord.Embed(title="ROCK🥌 PAPER🧻 SCISSOR✂", description=f"{rps_p2.mention} beat the crap out of {rps_p1.mention} through toss!", color=0xffff00)
        win_emb.set_thumbnail(url = rps_p2.display_avatar)
        await ctx.reply(embed = win_emb)

@client.command()
async def rpshelp(ctx):
    help_embed = nextcord.Embed(title = "🌟Kermy's Village🌟", description="🎮Rock, Paper, Scissor🎮", color=0xffff00)
    help_embed.set_thumbnail(url = ctx.author.display_avatar)
    help_embed.add_field(name="MORE INFO ABOUT THE GAME!", value="1.**\%rps [member1] [member2]**:Starts the game between these 2 players!.\n2.**\%gameover**:Ends the game and randomly chooses the winners!.\n3.The game may stuck sometimes due to a glitch or fault. Try starting a new one!.")
    await ctx.reply(embed = help_embed)
   
client.run("*****BOT-TOKEN******")
