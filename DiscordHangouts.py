# IMPORTING

import discord
import asyncio
from discord import Embed
from discord.ext import commands
from discord.utils import get
import sqlite3
import os
from collections import Counter
import random
import re

# VARIABLES
global Games
Games = {}
global Cards
Cards = {}
TOKEN = ""
BOT_PREFIX = "!"
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)
DIR = os.path.dirname(__file__)
db = sqlite3.connect(os.path.join(DIR, "BankAccounts.db"))
SQL = db.cursor()
db2 = sqlite3.connect(os.path.join(DIR, "Wallet.db"))
SQL2 = db2.cursor()
db3 = sqlite3.connect(os.path.join(DIR, "Raises.db"))
SQL3 = db3.cursor()
START_BALANCE = 100
C_NAME = ":money_with_wings:"
Random1 = ""
Random2 = ""
Random3 = ""
Random4 = ""
Random5 = ""
Random6 = ""
Random7 = ""
Random8 = ""
Random9 = ""
Random10 = ""
# CODE
@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}.")



async def findValues(Card1, Card2, Card3):
    Values = []
    Cards = [Card1, Card2, Card3]
    for Card in Cards:
        if str(Card)[2:3].isnumeric():
            Values.insert(0, (re.sub("[^0-9]", "", str(Card)[2:4])))
        else:
            
            if (str(Card)[2:3]) == "J":
                Values.insert(0, ("10"))
            elif (str(Card)[2:3]) == "Q":
                Values.insert(0, ("10"))
            elif (str(Card)[2:3]) == "K":
                Values.insert(0, ("10"))
            elif (str(Card)[2:3]) == "A":
                Values.insert(0, ("11"))

    return Values





async def findRandomCard():
    randoms = [Random4, Random5, Random6, Random7, Random8, Random9, Random10]
    RandomCard = ""
    for ran in randoms:
        if ran == "":
            RandomCard = ran

    return RandomCard


async def findNewValues(Card, Value):

    if str(Card)[2:3].isnumeric():
        Value = int(Value) + int(re.sub("[^0-9]", "", str(Card)[2:4]))
    else:
        if (str(Card)[2:3]) == "J" or (str(Card)[2:3]) == "Q" or (str(Card)[2:3]) == "K":
             Value = int(Value) + 10
        elif (str(Card)[2:3]) == "A":
            if 11 > int(Value):
                Value = int(Value) + 11
            else:
                Value = int(Value) + int(21 - int(Value))



    return Value

async def DealersCardsAndValue(Value1, Value2):
    String2 = ""
    val2 = int(Value2)
    emojis = []                                       
    for guild in bot.guilds:
        if guild.name != "Discord Hangouts":
            for emoji in guild.emojis:
                if str(emoji) != "<:cardBack:805838413823475712>":
                    emojis.insert(0, emoji)
    Cards = []
    ListofCards = []
    while True:
                
        if int(Value1) >= val2:
            val2 = int(Value2)
            newCard = random.choice(list(emojis))
            Cards.insert(len(Cards) - 1, str(newCard))
            String2 = String2 + str(newCard)
            for Card in Cards:
                if str(Card)[2:3].isnumeric():
                    val2 = int(val2) + int(re.sub("[^0-9]", "", str(Card)[2:4]))
                else:
                    if Cards[len(Cards) - 1] != Card:
                        if (str(Card)[2:3]) == "J":
                            val2 = int(val2) + int(10)
                        elif (str(Card)[2:3]) == "Q":
                            val2 = int(val2) + int(10)
                        elif (str(Card)[2:3]) == "K":
                            val2 = int(val2) + int(10)
                        elif (str(Card)[2:3]) == "A":
                            val2 = int(val2) + int(11)
                    else:
                        if (str(Card)[2:3]) == "A":
                            if int(val2) >= 11:
                                val2 = int(val2) + int(21 - int(val2))
                            else:
                                val2 = int(val2) + int(11)
                        else:
                            if str(Card)[2:3].isnumeric():
                                val2 = int(val2) + int(re.sub("[^0-9]", "", str(Card)[2:4]))
                            else:
                                if (str(Card)[2:3]) == "J":
                                    val2 = int(val2) + int(10)
                                elif (str(Card)[2:3]) == "Q":
                                    val2 = int(val2) + int(10)
                                elif (str(Card)[2:3]) == "K":
                                    val2 = int(val2) + int(10)
        else:
            return val2, String2


@bot.command(aliases=["tm"])
async def tempmute(ctx, member: discord.Member, time: int, d, *, reason=None):
    role = discord.utils.find(lambda r: r.name == 'Jupiter', ctx.guild.roles)
    role2 = discord.utils.find(lambda r: r.name == 'Member', ctx.guild.roles)
    if not role in ctx.author.roles:
        return
    guild = ctx.guild

    for role in guild.roles:
        if role.name == "Muted":
            await member.remove_roles(role2)
            await member.add_roles(role)

            embed = discord.Embed(title="Muted!", description=f"{member.mention} has been tempmuted ", colour=discord.Colour.light_gray())
            embed.add_field(name="Reason:", value=reason, inline=False)
            embed.add_field(name="Time left for the mute:", value=f"{time}{d}", inline=False)
            await ctx.send(embed=embed)

            if d == "s":
                await asyncio.sleep(time)

            if d == "m":
                await asyncio.sleep(time*60)

            if d == "h":
                await asyncio.sleep(time*60*60)

            if d == "d":
                await asyncio.sleep(time*60*60*24)

            await member.remove_roles(role)

            embed = discord.Embed(title="Unmuted", description=f"Unmuted -{member.mention} ", colour=discord.Colour.light_gray())
            await ctx.send(embed=embed)

            return

@bot.command(brief="Shows users their balance", aliases=["bal"])
async def balance(ctx, user: discord.Member = None):
    if user:
        USER_ID = user.id
        USER_NAME = str(user)
        SQL.execute(
            'create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)'
        )
        SQL2.execute(
            'create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)'
        )
        SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
        SQL2.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
        result_userID = SQL.fetchone()
        result2_userID = SQL2.fetchone()

        if result_userID is None:
            SQL.execute(
                "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
                (USER_NAME, USER_ID, START_BALANCE),
            )
            db.commit()

        if result2_userID is None:
            SQL2.execute(
                "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
                (USER_NAME, USER_ID, "0"),
            )
            db2.commit()

        SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
        SQL2.execute(f'select balance from Accounts where user_id="{USER_ID}"')

        result_userbal = SQL.fetchone()
        result2_userbal = SQL2.fetchone()
        await ctx.send(
            f"{user.mention} has a {round(result_userbal[0])} {C_NAME} in their bank account and {round(result2_userbal[0])} {C_NAME}  in their wallet."
        )
    else:
        USER_ID = ctx.message.author.id
        USER_NAME = str(ctx.message.author)
        SQL.execute(
            'create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)'
        )
        SQL2.execute(
            'create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)'
        )
        SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
        SQL2.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
        result_userID = SQL.fetchone()
        result2_userID = SQL2.fetchone()

        if result_userID is None:
            SQL.execute(
                "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
                (USER_NAME, USER_ID, START_BALANCE),
            )
            db.commit()

        if result2_userID is None:
            SQL2.execute(
                "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
                (USER_NAME, USER_ID, "0"),
            )
            db2.commit()

        SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
        SQL2.execute(f'select balance from Accounts where user_id="{USER_ID}"')

        result_userbal = SQL.fetchone()
        result2_userbal = SQL2.fetchone()
        await ctx.send(
            f"{ctx.message.author.mention} has a {round(result_userbal[0])} {C_NAME}  in their bank account and {round(result2_userbal[0])} {C_NAME} in their wallet."
        )


@bot.command(brief="Withdraw your money to your wallet.", aliases=["with"])
async def withdraw(ctx, money: str):
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    SQL.execute(
        'create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)'
    )
    SQL2.execute(
        'create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)'
    )
    SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    SQL2.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result_userID = SQL.fetchone()
    result2_userID = SQL2.fetchone()

    if result_userID is None:
        SQL.execute(
            "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
            (USER_NAME, USER_ID, START_BALANCE),
        )
        db.commit()

    if result2_userID is None:
        SQL2.execute(
            "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
            (USER_NAME, USER_ID, "0"),
        )
        db2.commit()

    SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    SQL2.execute(f'select balance from Accounts where user_id="{USER_ID}"')

    result_userbal = SQL.fetchone()
    result2_userbal = SQL2.fetchone()
    if money == "all":
        if result_userbal[0] == 0:
            await ctx.send("You do not have any money in your bank account.")
            return
        SQL.execute(
            "update Accounts set balance = balance - ? where user_id = ?",
            (result_userbal[0], USER_ID),
        )
        db.commit()
        SQL2.execute(
            "update Accounts set balance = balance + ? where user_id = ?",
            (result_userbal[0], USER_ID),
        )
        await ctx.send(
            f"{ctx.message.author.mention} just withdrew {round(result_userbal[0])}:money_with_wings: into their wallet."
        )
    else:
        if int(money) > int(result_userbal[0]):
            await ctx.send("You do not have enough money in your bank account.")
            return
        SQL.execute(
            "update Accounts set balance = balance - ? where user_id = ?",
            (int(money), USER_ID),
        )
        db.commit()
        SQL2.execute(
            "update Accounts set balance = balance  +  ? where user_id = ?",
            (int(money), USER_ID),
        )
        db2.commit()
        await ctx.send(
            f"{ctx.message.author.mention} just withdrew {int(money)}:money_with_wings: into their wallet."
        )
    return


@bot.command(brief="Deposit your money to your bank account.", aliases=["dep"])
async def deposit(ctx, money: str):
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    SQL.execute(
        'create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)'
    )
    SQL2.execute(
        'create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)'
    )
    SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    SQL2.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result_userID = SQL.fetchone()
    result2_userID = SQL2.fetchone()

    if result_userID is None:
        SQL.execute(
            "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
            (USER_NAME, USER_ID, START_BALANCE),
        )
        db.commit()

    if result2_userID is None:
        SQL2.execute(
            "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
            (USER_NAME, USER_ID, "0"),
        )
        db2.commit()

    SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    SQL2.execute(f'select balance from Accounts where user_id="{USER_ID}"')

    result_userbal = SQL.fetchone()
    result2_userbal = SQL2.fetchone()

    if money == "all":
        if result2_userbal[0] == 0:
            await ctx.send("You do not have any money in your wallet.")
            return
        SQL.execute(
            "update Accounts set balance = balance + ? where user_id = ?",
            (result2_userbal[0], USER_ID),
        )
        db.commit()
        SQL2.execute(
            "update Accounts set balance = balance - ? where user_id = ?",
            (result2_userbal[0], USER_ID),
        )
        db2.commit()
        await ctx.send(
            f"{ctx.message.author.mention} just deposited {round(result2_userbal[0])}:money_with_wings: into their bank account."
        )
    else:
        if int(money) > int(result2_userbal[0]):
            await ctx.send("You do not have enough money in your wallet.")
            return
        SQL2.execute(
            "update Accounts set balance = balance - ? where user_id = ?",
            (int(money), USER_ID),
        )
        db2.commit()
        SQL.execute(
            "update Accounts set balance = balance + ? where user_id = ?",
            (int(money), USER_ID),
        )
        db.commit()
        await ctx.send(
            f"{ctx.message.author.mention} just deposited {int(money)}:money_with_wings: into their bank account."
        )
    return


@bot.command(brief="list top 3 bank accounts", aliases=["top"])
async def top3(ctx):
    dictionary = {}
    for member in ctx.message.guild.members:
        mention = member.mention
        USER_ID = member.id
        USER_NAME = str(member)
        SQL.execute(
            'create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)'
        )
        SQL2.execute(
            'create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)'
        )
        SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
        SQL2.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
        result_userID = SQL.fetchone()
        result2_userID = SQL2.fetchone()

        if result_userID is None:
            SQL.execute(
                "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
                (USER_NAME, USER_ID, START_BALANCE),
            )
            db.commit()

        if result2_userID is None:
            SQL2.execute(
                "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
                (USER_NAME, USER_ID, "0"),
            )
            db2.commit()

        SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
        SQL2.execute(f'select balance from Accounts where user_id="{USER_ID}"')

        result_userbal = SQL.fetchone()
        result2_userbal = SQL2.fetchone()
        dictionary[USER_NAME] = str(result_userbal[0] + result2_userbal[0])

    k = Counter(dictionary)
    high = k.most_common(3)
    embed = discord.Embed(title="Top 3 Net Worths", color=0x057BFA)
    author = ctx.message.author
    pfp = author.avatar_url
    embed.set_author(name=USER_NAME, icon_url=str(pfp))
    for i in high:
        embed.add_field(
            name=i[0],
            value=(str(int(float(i[1]))) + ":money_with_wings:"),
            inline=False,
        )
    await ctx.send(embed=embed)


@bot.command(brief="Pay Someone", aliases=["pay", "give"])
async def transfer(ctx, other: discord.Member, amount: int):
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    OTHER_ID = other.id
    OTHER_NAME = str(other)

    SQL2.execute(
        'create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)'
    )
    SQL2.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result_userID = SQL2.fetchone()
    SQL2.execute(f'select user_id from Accounts where user_id="{OTHER_ID}"')
    result_otherID = SQL2.fetchone()

    if result_userID is None:
        SQL2.execute(
            "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
            (USER_NAME, USER_ID, 0),
        )
        db2.commit()
    if result_otherID is None:
        SQL2.execute(
            "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
            (OTHER_NAME, OTHER_ID, 0),
        )
        db2.commit()

    SQL2.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    result_userbal = SQL2.fetchone()
    if amount > int(result_userbal[0]):
        await ctx.send(
            f"{ctx.message.author.mention} does not have that many :money_with_wings:"
        )
        return

    SQL2.execute(
        "update Accounts set balance = balance - ? where user_id = ?", (amount, USER_ID)
    )
    db2.commit()
    SQL2.execute(
        "update Accounts set balance = balance + ? where user_id = ?",
        (amount, OTHER_ID),
    )
    db2.commit()

    await ctx.send(
        f"{ctx.message.author.mention} sent {other.mention} {amount} :money_with_wings:"
    )


@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command(brief="Work to get money")
async def work(ctx):
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    SQL.execute(
        'create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)'
    )
    SQL2.execute(
        'create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)'
    )
    SQL3.execute(
        'create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)'
    )
    SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    SQL2.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    SQL3.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result_userID = SQL.fetchone()
    result2_userID = SQL2.fetchone()
    result3_userID = SQL3.fetchone()

    if result_userID is None:
        SQL.execute(
            "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
            (USER_NAME, USER_ID, START_BALANCE),
        )
        db.commit()

    if result2_userID is None:
        SQL2.execute(
            "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
            (USER_NAME, USER_ID, "0"),
        )
        db2.commit()

    if result3_userID is None:
        SQL3.execute(
            "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
            (USER_NAME, USER_ID, "0"),
        )
    db3.commit()

    SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    SQL2.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    SQL3.execute(f'select balance from Accounts where user_id="{USER_ID}"')

    result_userbal = SQL.fetchone()
    result2_userbal = SQL2.fetchone()
    result3_userbal = SQL3.fetchone()

    if result3_userbal[0] < 5:
        amount = int(random.randint(20, 50))
        SQL2.execute(
            "update Accounts set balance = balance + ? where user_id = ?",
            (amount, USER_ID),
        )
        db2.commit()
        SQL3.execute(
            "update Accounts set balance = balance + ? where user_id = ?",
            (int(1), USER_ID),
        )
        db3.commit()
        await ctx.send(
            f"{ctx.message.author.mention} earned {amount}:money_with_wings: for working!"
        )

    if result3_userbal[0] == 5:
        await ctx.send(f"{ctx.message.author.mention} just got a raise!")

    if result3_userbal[0] > 4 and not result3_userbal[0] > 9:
        amount = int(random.randint(50, 80))
        SQL2.execute(
            "update Accounts set balance = balance + ? where user_id = ?",
            (amount, USER_ID),
        )
        db2.commit()
        SQL3.execute(
            "update Accounts set balance = balance + ? where user_id = ?",
            (int(1), USER_ID),
        )
        db3.commit()
        await ctx.send(
            f"{ctx.message.author.mention} earned {amount}:money_with_wings: for working!"
        )

    if result3_userbal[0] == 10:
        await ctx.send(f"{ctx.message.author.mention} just got their second raise!")

    if result3_userbal[0] > 9 and not result3_userbal[0] > 14:
        amount = int(random.randint(100, 160))
        SQL2.execute(
            "update Accounts set balance = balance + ? where user_id = ?",
            (amount, USER_ID),
        )
        db2.commit()
        SQL3.execute(
            "update Accounts set balance = balance + ? where user_id = ?",
            (int(1), USER_ID),
        )
        db3.commit()
        await ctx.send(
            f"{ctx.message.author.mention} earned {amount}:money_with_wings: for working!"
        )

    if result3_userbal[0] == 30:
        await ctx.send(f"{ctx.message.author.mention} just got their final raise!")

    if result3_userbal[0] > 29:
        amount = int(
            ((result_userbal[0] + result2_userbal[0]) * int(random.randint(10, 25)))
            / 100
        )
        SQL2.execute(
            "update Accounts set balance = balance + ? where user_id = ?",
            (amount, USER_ID),
        )
        db2.commit()
        SQL3.execute(
            "update Accounts set balance = balance + ? where user_id = ?",
            (int(1), USER_ID),
        )
        db3.commit()
        await ctx.send(
            f"{ctx.message.author.mention} earned {amount}:money_with_wings: for working!"
        )

@commands.cooldown(1, 60, commands.BucketType.user)
@bot.command(brief="Do some bad thing to get money, but if you're unlucky, you'll lose money!")
async def crime(ctx):
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    SQL.execute(
        'create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)'
    )
    SQL2.execute(
        'create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)'
    )
    SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    SQL2.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result_userID = SQL.fetchone()
    result2_userID = SQL2.fetchone()

    if result_userID is None:
        SQL.execute(
            "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
            (USER_NAME, USER_ID, START_BALANCE),
        )
        db.commit()

    if result2_userID is None:
        SQL2.execute(
            "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
            (USER_NAME, USER_ID, "0"),
        )
        db2.commit()

    SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    SQL2.execute(f'select balance from Accounts where user_id="{USER_ID}"')

    result_userbal = SQL.fetchone()
    result2_userbal = SQL2.fetchone()

    successmessages = ["You steal change from the homeless. You got", "You steal an orange and pawn it for", "You start up a detective service for a few days, but when you finally get business you end up robbing your client for", "You work for a Mexican cartel and make", "You break into a home to steal jewelry worth", "You commit a heist and manage to take", "You hacked this server and got", "You steal a guard's radio and sell it for parts, and receive", "You steal candy and sell it on the black market for"]
    unsuccessmessages = ["Steal an extra gram of cocaine from your dealer, Sarah, and get caught. To dodge death, you paid", "You attempted to rob the local bank and got caught by the police. You are fined", "The cops start chasing, you and your wallet falls out. You lost", "You were caught lying at a truth or dare question! The fine is", "During a drug deal with a notorious drug cartel, they jump the gun and take both your paid drugs and wallet. You lost", "someone catches you in the act. You lose your Youtube channel you worked so hard on and", "You got caught hacking into the CIA, and lost", "You were caught not helping to commit the crime, and just being lazy on Discord. For this you've been fined", "You tried to jump the old lady walking down the street. Turns out she had a gun, and robbed you blind of", "You got caught stealing from a donations jar and in return you get fined", "You failed stealing candy from a kid and got fined", "You attempt to steal, but the person stabs you. Hospital expenses hate you, so you lost", "You were jaywalking, so you lost", "You stabbed a officer to take his money but he fought back and he stabbed you, the medical bill was", "A wise asian girl once said, Be a better criminal. Get fined", "You were found in the Springfield Power Plant trying to make crack cocaine, you were fined"]


    if random.randint(1, 2) == 1:
        amount = int(((result_userbal[0] + result2_userbal[0]) * int(random.randint(10, 25)))/ 100)
        await ctx.send(f"{random.choice(successmessages)} {amount}:money_with_wings: ")
        SQL2.execute(
            "update Accounts set balance = balance + ? where user_id = ?",
            (amount, USER_ID),
        )
        db2.commit()

    else:
        
        amount = int(((result_userbal[0] + result2_userbal[0]) * int(random.randint(5, 25)))/ 100)
        await ctx.send(f"{random.choice(unsuccessmessages)} {amount}:money_with_wings: ")

        SQL2.execute(
            "update Accounts set balance = balance - ? where user_id = ?",
            (amount, USER_ID),
        )
        db2.commit()

@bot.command(brief="Rob Someone", aliases=["steal", "take"])
async def rob(ctx, other: discord.Member):
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    OTHER_ID = other.id
    OTHER_NAME = str(other)

    SQL2.execute(
        'create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)'
    )
    SQL2.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result2_userID = SQL2.fetchone()

    if result2_userID is None:
        SQL2.execute(
            "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
            (USER_NAME, USER_ID, "0"),
        )
        db2.commit()

    SQL2.execute(f'select balance from Accounts where user_id="{USER_ID}"')

    result2_userbal = SQL2.fetchone()

    SQL2.execute(
        'create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)'
    )
    SQL2.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result2_otherID = SQL2.fetchone()


    if result2_otherID is None:
        SQL2.execute(
            "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
            (OTHER_NAME, OTHER_ID, "0"),
        )
        db2.commit()

    SQL2.execute(f'select balance from Accounts where user_id="{OTHER_ID}"')

    result2_otherbal = SQL2.fetchone()

    if random.randint(1, 2) == 1:
        amount = int(((result2_otherbal[0]) * int(random.randint(5, 40)))/ 100)
        SQL2.execute(
            "update Accounts set balance = balance - ? where user_id = ?",
            (amount, OTHER_ID),
        )
        db2.commit()
        SQL2.execute(
            "update Accounts set balance = balance + ? where user_id = ?",
            (amount, USER_ID),
        )
        db2.commit()
        await ctx.send(f"{ctx.message.author.mention} successfully robbed {amount}:money_with_wings:  from <@{OTHER_ID}>!")
    else:
        amount = int(((result2_otherbal[0]) * int(random.randint(5, 40)))/ 100)
        SQL2.execute(
            "update Accounts set balance = balance - ? where user_id = ?",
            (amount, USER_ID),
        )
        db2.commit()
        await ctx.send(f"{ctx.message.author.mention} failed to rob <@{OTHER_ID}>, so he lost {amount}:money_with_wings: ")


@bot.command(brief="Chicken Fight to get money", aliases=["cf", "cock-fight","chicken-fight"])
async def fight(ctx, amount: int):
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    SQL2.execute(
        'create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)'
    )
    SQL2.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result2_userID = SQL2.fetchone()

    if result2_userID is None:
        SQL2.execute(
            "insert into Accounts(user_name, user_id, balance) values(?,?,?)",
            (USER_NAME, USER_ID, "0"),
        )
        db2.commit()

    SQL2.execute(f'select balance from Accounts where user_id="{USER_ID}"')

    result2_userbal = SQL2.fetchone()

    if result2_userbal[0] > (amount - 1):
        if random.randint(1, 2) == 1:
            SQL2.execute("update Accounts set balance = balance + ? where user_id = ?",(amount, USER_ID))
            await ctx.send(f"Your chicken won the fight, and made you {amount}:money_with_wings: richer!")
        else:
            SQL2.execute("update Accounts set balance = balance - ? where user_id = ?",(amount, USER_ID))
            await ctx.send(f"Your chicken lost the fight, so you lost {amount}:money_with_wings:!")


@bot.command(brief="Play a game of black jack", aliases=["bj"])
async def blackjack(ctx, amount: int):

    idk = True
    amt = amount
    String = ""
    Randoms = 3
    USER_ID = ctx.message.author.id
    global Games


    USER_NAME = str(ctx.message.author)

    if USER_NAME in Games:
        return

    SQL2.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
    SQL2.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result2_userID = SQL2.fetchone()

    if result2_userID is None:
        SQL2.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (USER_NAME, USER_ID, 100))
        db2.commit()

        

    SQL2.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    result2_userbal = SQL2.fetchone()

    if amount < 99:
        await ctx.send("The amount must be at least 100!")
    elif result2_userbal[0] < (amount - 1):
        await ctx.send("You don't have enough money!")
    else:
        emojis = []
        for guild in bot.guilds:
            if guild.name != "Discord Hangouts":
                for emoji in guild.emojis:
                    if str(emoji) != "<:cardBack:805838413823475712>":
                        emojis.insert(1, emoji)
        Random1 = random.choice(list(emojis))
        Random2 = random.choice(list(emojis))
        Random3 = random.choice(list(emojis))
        Values = await findValues(Random1, Random2, Random3)
        Value1 = int(Values[1]) + int(Values[2])        
        Value2 = Values[0]
        Title = "Type hit to draw a card, double down to double down or stand to pass."
        if Value1 >= int(21):
            idk = False
            Value1 = "Blackjack!"
            Title = f"You won the game. You earned {amt} {C_NAME}"
            SQL2.execute(
                "update Accounts set balance = balance + ? where user_id = ?", (amt, USER_ID)
            )
            db2.commit()
        else:
            Cards[USER_NAME] = str(amt) + " " + str(Random1) + " " + str(Random2) + " " + str(Random3) + " " + str(Value1) + " " + str(Value2)
        
        author = ctx.message.author
        pfp = author.avatar_url

        embed = Embed(title=Title)
        embed.set_author(name=author, icon_url=str(pfp))
        embed.add_field(name="**Your Hand**", value=f"\n {Random1} {Random2}\n\nValue: {Value1}", inline=True)
        embed.add_field(name="**Dealer Hand**", value=f"\n {Random3} <:cardBack:805838413823475712>\n\nValue: {Value2}", inline=True)
        embed.set_footer(text="From Discord Hangout's Bot")
        blackjackmessage = await ctx.send(embed=embed)
        if idk != False:
            Games[USER_NAME] = blackjackmessage


@bot.event
async def on_message(message):
    cards = []
    global Games
    if str(message.author) in Games:
        if message.content == "hit":
            USER_ID = message.author.id
            card = Cards[str(message.author)].split()
            amt = card[0]
            Random1 = card[1]
            Random2 = card[2]
            Random3 = card[3]
            Value1 = card[4]
            Value2 = card[5]
            String = ""

            if len(Cards[str(message.author)].split()) >= 7:
                String = ""
                for i in range(6, len(Cards[str(message.author)].split())):
                    String = String + card[i]
            else:
                String = ""
            emojis = []                                       
            for guild in bot.guilds:
                if guild.name != "Discord Hangouts":
                    for emoji in guild.emojis:
                        if str(emoji) != "<:cardBack:805838413823475712>":
                            emojis.insert(1, emoji)
            RandomCard = await findRandomCard()
            globals()[RandomCard] = random.choice(list(emojis))
            cards.insert(len(cards), globals()[RandomCard])
            for card in cards:
                if String == "":
                    String = str(card)
                else:
                    String = String + " " + str(card)
            Value1 = await findNewValues(globals()[RandomCard], Value1)

            Cards[str(message.author)] = str(amt) + " " + str(Random1) + " " + str(Random2) + " " + str(Random3) + " " + str(Value1) + " " + str(Value2) + " " + String

            Title = "Type hit to draw a card, double down to double down or stand to pass."
            something = Value1
            if Value1 == int(21):

                Value1 = "Blackjack!"
                Title = f"You won the game. You earned {amt} {C_NAME}"
                SQL2.execute(
                    "update Accounts set balance = balance + ? where user_id = ?", (amt, USER_ID)
                )
                db2.commit()
            elif Value1 > int(21):
                Title = f"You lost the game. You lost {amt} {C_NAME}"
                SQL2.execute(
                    "update Accounts set balance = balance - ? where user_id = ?", (amt, USER_ID)
                )
                db2.commit()
            Values = await findValues(Random1, Random2, Random3) 
            Value2 = Values[0]
            author = message.author
            pfp = author.avatar_url
            embed = Embed(title=Title)
            embed.set_author(name=str(author), icon_url=str(pfp))
            embed.add_field(name="**Your Hand**", value=f"\n {Random1} {Random2} {String}\n\nValue: {Value1}", inline=True)
            embed.add_field(name="**Dealer Hand**", value=f"\n {Random3} <:cardBack:805838413823475712>\n\nValue: {Value2}\n", inline=True)
            embed.set_footer(text="From Discord Hangout's Bot")
            msg = Games[str(message.author)]
            blackjackmessage = await msg.edit(embed=embed)
            if something == int(21):
                Games.pop(str(message.author))
                Cards.pop(str(message.author))
            elif something > int(21):
                Games.pop(str(message.author))
                Cards.pop(str(message.author))
            else:
                if not Games[str(message.author)]:
                    Games[str(message.author)] = blackjackmessage
        elif message.content == "stand":
            card = Cards[str(message.author)].split()
            amt = card[0]
            Random1 = card[1]
            Random2 = card[2]
            Random3 = card[3]
            Value1 = card[4]
            Value2 = card[5]
            String = ""
            String2 = ""


            if len(Cards[str(message.author)].split()) >= 7:
                for i in range(6, len(Cards[str(message.author)].split())):
                    String2 = String2 + card[i]
            result = await DealersCardsAndValue(Value1, Value2)

            if len(Cards[str(message.author)].split()) >= 7:
                String = ""
                for i in range(6, len(Cards[str(message.author)].split())):
                    String = String + card[i]


            
            Value2 = result[0]
            String2 = result[1]
            Title = ""

            if int(Value1) == int(Value2):
                Title = "It was a draw. You got your money back."
            elif int(Value2) == 21:
                Title = f"You lost the game. You lost {amt} {C_NAME}"
                SQL2.execute(
                    "update Accounts set balance = balance - ? where user_id = ?", (amt, message.author.id)
                )
                db2.commit()
            elif int(Value2) > 21:
                Title = f"You won the game. You earned {amt} {C_NAME}"
                SQL2.execute(
                    "update Accounts set balance = balance + ? where user_id = ?", (amt, message.author.id)
                )
                db2.commit()
            elif int(Value1) > int(Value2):
                Title = f"You won the game. You earned {amt} {C_NAME}"
                SQL2.execute(
                    "update Accounts set balance = balance + ? where user_id = ?", (amt, message.author.id)
                )
                db2.commit()
            elif int(Value2) > int(Value1):
                Title = f"You lost the game. You lost {amt} {C_NAME}"
                SQL2.execute(
                    "update Accounts set balance = balance - ? where user_id = ?", (amt, message.author.id)
                )
                db2.commit()
            else:
                Title = "Not sure what the outcome of the game is; the game will be considered as a draw."



            author = message.author
            pfp = author.avatar_url
            embed = Embed(title=Title)
            embed.set_author(name=str(author), icon_url=str(pfp))
            embed.add_field(name="**Your Hand**", value=f"\n {Random1} {Random2} {String}\n\nValue: {Value1}", inline=True)
            embed.add_field(name="**Dealer Hand**", value=f"\n {Random3} {String2}\n\nValue: {Value2}", inline=True)
            embed.set_footer(text="From Discord Hangout's Bot")
            msg = Games[str(message.author)]
            blackjackmessage = await msg.edit(embed=embed)
            Games.pop(str(message.author))
        elif message.content == "double down" or message.content == "db":
            card = Cards[str(message.author)].split()
            amt = card[0]
            amt = int(amt)*2
            Random1 = card[1]
            Random2 = card[2]
            Random3 = card[3]
            Value1 = card[4]
            Value2 = card[5]
            String = ""
            String2 = ""

            if len(Cards[str(message.author)].split()) >= 7:
                String = ""
                for i in range(6, len(Cards[str(message.author)].split())):
                    String = String + card[i]
            else:
                String = ""

            if len(Cards[str(message.author)].split()) >= 7:
                for i in range(6, len(Cards[str(message.author)].split())):
                    String2 = String2 + card[i]
            emojis = []                                       
            for guild in bot.guilds:
                if guild.name != "Discord Hangouts":
                    for emoji in guild.emojis:
                        if str(emoji) != "<:cardBack:805838413823475712>":
                            emojis.insert(1, emoji)
            RandomCard = await findRandomCard()
            globals()[RandomCard] = random.choice(list(emojis))
            cards.insert(len(cards), globals()[RandomCard])
            for card in cards:
                String = String + " " + str(card)
            Value1 = await findNewValues(globals()[RandomCard], Value1)


            if int(Value1) <= 21:
                result = await DealersCardsAndValue(Value1, Value2)
                Value2 = result[0]
                String2 = result[1]
                if int(Value1) == int(Value2):
                    Title = "It was a draw. You got your money back."
                elif int(Value1) == 21: 
                    Title = f"You won the game. You earned {amt} {C_NAME}"
                    SQL2.execute(
                        "update Accounts set balance = balance + ? where user_id = ?", (amt, message.author.id)
                    )
                    db2.commit()
                elif int(Value2) == 21:
                    Title = f"You lost the game. You lost {amt} {C_NAME}"
                    SQL2.execute(
                        "update Accounts set balance = balance - ? where user_id = ?", (amt, message.author.id)
                    )
                    db2.commit()
                elif int(Value1) > 21:
                    Title = f"You lost the game. You lost {amt} {C_NAME}"
                    SQL2.execute(
                        "update Accounts set balance = balance - ? where user_id = ?", (amt, message.author.id)
                    )
                    db2.commit()
                elif int(Value2) > 21:
                    Title = f"You won the game. You earned {amt} {C_NAME}"
                    SQL2.execute(
                        "update Accounts set balance = balance + ? where user_id = ?", (amt, message.author.id)
                    )
                    db2.commit()
                elif int(Value1) > int(Value2):
                    Title = f"You won the game. You earned {amt} {C_NAME}"
                    SQL2.execute(
                        "update Accounts set balance = balance + ? where user_id = ?", (amt, message.author.id)
                    )    
                    db2.commit()
                elif int(Value1) < int(Value2):
                    Title = f"You lost the game. You lost {amt} {C_NAME}"
                    SQL2.execute(
                        "update Accounts set balance = balance - ? where user_id = ?", (amt, message.author.id)
                    )
                    db2.commit()
                else:
                    Title = "Not sure what the outcome of the game is; the game will be considered as a draw."
                author = message.author
                pfp = author.avatar_url
                embed = Embed(title=Title)
                embed.set_author(name=str(author), icon_url=str(pfp))
                embed.set_author(name=str(author), icon_url=str(pfp))
                embed.add_field(name="**Your Hand**", value=f"\n {Random1} {Random2} {String}\n\nValue: {Value1}", inline=True)
                embed.add_field(name="**Dealer Hand**", value=f"\n {Random3} {String2}\n\nValue: {Value2}", inline=True)
                embed.set_footer(text="From Discord Hangout's Bot")
                msg = Games[str(message.author)]
                blackjackmessage = await msg.edit(embed=embed)
                Games.pop(str(message.author))
            else:
                author = message.author
                pfp = author.avatar_url
                embed = Embed(title=f"You lost the game. You lost {amt} {C_NAME}")
                embed.set_author(name=str(author), icon_url=str(pfp))
                embed.set_author(name=str(author), icon_url=str(pfp))
                embed.add_field(name="**Your Hand**", value=f"\n {Random1} {Random2} {String}\n\nValue: {Value1}", inline=True)
                embed.add_field(name="**Dealer Hand**", value=f"\n {Random3} <:cardBack:805838413823475712>\n\nValue: {Value2}", inline=True)
                embed.set_footer(text="From Discord Hangout's Bot")
                msg = Games[str(message.author)]
                blackjackmessage = await msg.edit(embed=embed)
                Games.pop(str(message.author))
                SQL2.execute(
                    "update Accounts set balance = balance - ? where user_id = ?", (amt, message.author.id)
                )
                db2.commit()
   

    await bot.process_commands(message)




# RUNNING THE BOT
bot.run(TOKEN)
