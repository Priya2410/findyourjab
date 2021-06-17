# importing discord.py
from cowin_api.utils import today
import discord

#importing date 
from datetime import date

#importing cowin 
from cowin_api import api
cowin = api.CoWinAPI()

#This is only for Karnataka and its districs
state_id=16 #state id for Karnataka
dist=cowin.get_districts(state_id=16)
bangalore_rural=276 #district_id
bangalore_urban=265 #district_name
bbmp=294 #BBMP

print(date.today())
date_today=str(date.today())
date_new=date_today.split('-')
date_new=date_new[::-1]
today_date= "-"
today_date = today_date.join(date_new)
my_district=int()

#client
client = discord.Client()

# registers an event for client - discord bot
@client.event
async def on_connect():
    general= client.get_channel() #    general= client.get_channel(Enter your discord channel id here)
    embed=discord.Embed(
        title="Hello welcome to "+client.user.name,
        description="Here are some guidelines to start with the bot",
        color=discord.Color.random()
    )
    embed.add_field(name="**Bengaluru Rural**",value="Enter BR or br for finding vaccines in Bengaluru Rural",inline=False)
    embed.add_field(name="**Bengaluru Urban**",value="Enter BU or bu for finding vaccines in Bengaluru Urban",inline=False)
    embed.add_field(name="**BBMP**",value="Enter BBMP or bbmp for finding vaccines in BBMP",inline=False)
    await general.send(embed=embed)

@client.event
async def display(my_dis):
    general= client.get_channel()     #general= client.get_channel(Enter your discord channel id here)
    if(my_dis!=-1):
        vaccine=cowin.get_availability_by_district(str(my_dis),today_date)
        for i in vaccine['centers']:
            for j in i['sessions']:
                string=" "
                if j['date']==today_date:
                    if(j['available_capacity']>0 and j['min_age_limit']==18):
                        embed=discord.Embed(
                                title="Vaccine @ "+i['name'],
                                color=discord.Color.green()
                        )
                        embed.add_field(name="**Address**",value=i['address'],inline=False)
                        embed.add_field(name="**Date**",value=j['date'],inline=False)
                        embed.add_field(name="**Pincode**",value=i['pincode'],inline=False)
                        embed.add_field(name="**Fee Type**",value=i['fee_type'],inline=False)
                        embed.add_field(name="**Vaccine Available**",value=j['vaccine'],inline=False)
                        embed.add_field(name="**Age Limit**",value=j['min_age_limit'],inline=False)
                        if(i['fee_type']!='Free'):
                            val=j['vaccine']
                            for p in i['vaccine_fees']:
                                if p['vaccine']==val:
                                    embed.add_field(name="**Fee is**",value=p['fee'],inline=False)
                        if(j['available_capacity_dose1']>0):
                            embed.add_field(name="**Capacity for dose 1**",value=j['available_capacity_dose1'],inline=False)
                        if(j['available_capacity_dose2']>0):
                            embed.add_field(name="**Capacity for dose 2**",value=j['available_capacity_dose2'],inline=False)
                        for sl in j['slots']:
                            string = string + sl + "\n"
                        embed.add_field(name="**Slots**",value=string,inline=False)
                        await general.send(embed=embed)
    else:
        embed=discord.Embed(
                title="Warning",
                description="Wrong ",
                color=discord.Color.red()
        )
        embed.add_field(name="**WHY**",value="You have entered the wrong value",inline=False)
        await general.send(embed=embed)


@client.event
async def on_message(message):
    if(message.content!=""):
        if(message.content=="BR" or message.content=="br"):
            my_district=bangalore_rural
            await display(my_district)
        elif(message.content=="BU" or message.content=="bu"):
            my_district=bangalore_urban
            await display(my_district)
        elif(message.content=="BBMP" or message.content=="bbmp"):
            my_district=bbmp
            await display(my_district)
        else:
            my_district=-1
            await display(my_district)

# To run client on the server
client.run('enter your discord token here')
