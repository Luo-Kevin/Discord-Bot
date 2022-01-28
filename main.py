import discord
import discord_fcn
import datetime as dt
import twitterMain as twitter
from keep_alive import keep_alive
from send import *
from twitterMain import TIME
import os


client = discord.Client()
token = os.environ.get("TOKEN")

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$today"):
        prov = "QC"
        code = "2406"
        province = "Quebec"
        id = twitter.ID
        time = twitter.TIME

        dataProv = data(prov)
        dataReg = data(code)
        dashContent = twitter.textContent(id, time)
        dashUrl = twitter.imageUrl(id, time)
        dash = f"""{dashContent}\n{dashUrl}"""

        msgData = combineMsgProvCity(
            province, dataProv, dataReg) + dash
        await message.channel.send(msgData)

    if message.content.startswith("$prov"):
        usrCmd = message.content.split("$prov")[1].strip()
        comLgt = usrCmd.split(" ")
        prov = comLgt[0]

        if len(comLgt) == 1:

            msg = discord_fcn.correct_word(prov)
            await message.channel.send(msg)
        elif len(comLgt) == 2:
            date = comLgt[1]
            msg = discord_fcn.correct_word(prov, date)
            await message.channel.send(msg)

        else:
            msg = "Invalid. Please read channel prov Province description"
            await message.channel.send(msg)

    if message.content.startswith("$news"):
        prov = message.content.split("$news")[1].strip()
        news = newsDataMsg(prov)
        await message.channel.send(news)

    if message.content.startswith("$help"):
        helpMsg = f"""```$today - Data of COVID in Quebec and Montreal with most recent Quebec Dashboard\n$prov [Province] - COVID data in a specific province (supports autocorrect for province names)\n$news [Province] - COVID news in a specific province (can search news other than Canada)\n$yesterday [Province] - COVID data from yesterday (Supports autocorrect for provinces)\n$rankingo [sortBy]- Ranks the provinces by the sortBy entry. \n\tSortBy defaults with active cases (supports autocorrect with sortBy commands).\n\t sortBy commands: ["active_cases", "active_cases_change", "avaccine", "cases", "cumulative_avaccine","cumulative_cases", "cumulative_cvaccine", "cumulative_deaths", "cumulative_dvaccine", "cumulative_recovered", "cumulative_testing", "recovered", "testing", "deaths"]\n$rankingd [date][sortBy]- Ranks the provinces by the sortBy entry with data specified in the date field. \n\tSortBy defaults with active cases (supports autocorrect with sortBy commands).\n\t sortBy commands: ["active_cases", "active_cases_change", "avaccine", "cases", "cumulative_avaccine","cumulative_cases", "cumulative_cvaccine", "cumulative_deaths", "cumulative_dvaccine", "cumulative_recovered", "cumulative_testing", "recovered", "testing", "deaths"]\n$dashboard [date] - Takes Quebec COVID dashboards depending on the date specified in the date parameter. \n\t Defaults with the most recent dashboard\n

        ```"""
        await message.channel.send(helpMsg)

    if message.content.startswith("$yesterday"):
        provYes = message.content.split("$yesterday")
        provD = provYes[1].strip().capitalize()
        print(provD)
        yesterday = str(nowDate - dt.timedelta(days=1))
        dataYesMsg = discord_fcn.correct_word(provD, yesterday)
        await message.channel.send(dataYesMsg)

    if message.content.startswith("$rankingo"):
        rankingCommand = message.content.split("$rankingo")
        rankingCommand.pop(0)

        if len(rankingCommand) == 1:
            if rankingCommand[0] == "":
                ranking = discord_fcn.ranking(date = None, sortBy = "active_cases")
                await message.channel.send(ranking)

            elif rankingCommand[0] != "":

                dateRanking = rankingCommand[0].strip()
                if dateRanking[:2].isdigit() and dateRanking[3:5].isdigit() and dateRanking[6:10].isdigit():

                    msg2paramRank = discord_fcn.ranking(date = None, sortBy = dateRanking)
                    await message.channel.send(msg2paramRank)

                else:
                    print(dateRanking)
                    msg2paramRank = discord_fcn.ranking(
                        "", dateRanking)
                    await message.channel.send(msg2paramRank)

    if message.content.startswith("$rankingd"):
        rankingCommand = message.content.split("$rankingd")
        rankingCommand.pop(0)
        newCommands = []
        temp = rankingCommand[0].strip().split(" ")
        print(temp)
        msg3paramRank = ""
        for i in temp:
            if i != "":
                newCommands.append(i)
        if len(newCommands) <= 3:
            dateRanking = newCommands[0]
            sortByCommand = ""
            if len(newCommands) == 2:
                sortByCommand = newCommands[1]
            elif len(newCommands) == 3:
                sortByCommand = newCommands[1] + "_" + newCommands[2]
            msg3paramRank = discord_fcn.ranking(
            date = dateRanking, sortBy = sortByCommand)
            print(sortByCommand)
            await message.channel.send(msg3paramRank)
        else:
            await message.channel.send(f"Invalid. Too many entries. Please enter $ranking [date] [sortBy]")

    if message.content.startswith("$dash"):
        content = message.content.split("$dash")
        id = twitter.ID
        date = content[1].strip()
        time = twitter.TIME
        if date != "":
            dashContent = twitter.textContent(id, date)
            dashUrl = twitter.imageUrl(id, date)
            dash = f"""{dashContent}\n{dashUrl}"""
            await message.channel.send(dash)
        else:
            dashContent = twitter.textContent(id, time)
            dashUrl = twitter.imageUrl(id, time)
            dash = f"""{dashContent}\n{dashUrl}"""
            await message.channel.send(dash)

keep_alive()
client.run(token)

