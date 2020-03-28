import smtplib, ssl, discord, logging, time, random
from discord.ext import commands, tasks
from itertools import cycle
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

prefix = "Bonzi, "
client = commands.Bot(command_prefix = prefix)
status = cycle(["Bonzi Buddy","Let's do something!",f"Using prefix {prefix}"])
with open("bonzi.jokes") as jokesFile:
    jokes = jokesFile.read().splitlines()
with open("bonzi.facts") as factsFile:
    facts = factsFile.read().splitlines()
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
client.remove_command("help")

@client.event
async def on_ready():
    change_status.start()
    print(f"Bot logged in.")

@client.event
async def on_member_join(member):
    print(f"{member} joined the server.")

@client.event
async def on_member_remove(member):
    print(f"{member} left the server.")

@client.command()
async def ping(ctx):
    await ctx.send(f"Current ping: {round(client.latency*1000)}ms")

@tasks.loop(seconds=15)
async def change_status():
    global prefix
    await client.change_presence(activity=discord.Game(next(status)))

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)

@client.command()
async def joke(ctx):
    selectedQuestion = random.randint(0,29)*2
    question = jokes[selectedQuestion]
    answer = jokes[selectedQuestion+1]
    await ctx.send(question)
    time.sleep(2)
    await ctx.send(answer)

@client.command()
async def fact(ctx):
    await ctx.send(random.choice(facts))

@client.command()
async def email(ctx, recemail, *message):
    if recemail == "" or message == "":
        await ctx.send("I need to know who/what to send!")
    sendmsg = " ".join(message)
    await ctx.send(f"Sending '{sendmsg}' to '{recemail}'")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"A message from {ctx.author}"
    content = MIMEText(f"{ctx.author} on Discord says: {sendmsg}", "plain")
    msg.attach(content)
    port = 465
    password = "ICanEmail!"
    sendemail = "discordbonzibot@gmail.com"
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sendemail, password)
        server.sendmail(sendemail,recemail,msg.as_string())

@client.command()
async def help(ctx):
    commands={}
    commands["joke"]="Gives a random joke!"
    commands["fact"]="Gives a random fact!"
    commands["email [email] [message]"]="Sends an email to [email] containing [message]"
    msg=discord.Embed(title='Bonzi Bot', description="Written by JezzaR The Protogen#6483 using Discord.py",color=0x543A77)
    for command,description in commands.items():
        msg.add_field(name=command,value=description, inline=False)
    await ctx.send("", embed=msg)

client.run("NjkyNTA5ODQ2NDk0MjQ5MDIw.Xnvk7Q.dWLGUbPwrFumwDpZ3gp_7Z3pizo")
