import discord
import random

TOKEN = 'seu token aqui'
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
client = discord.Client(intents=intents)

voice_states = {}

top_lane_champions = [
    'Aatrox', 'Akali', 'Akshan', 'Camille', 'Cho\'Gath', 'Darius', 'Dr.Mundo',
    'Fiora', 'Garen', 'Gangplank', 'Gragas', 'Gwen', 'Heimer', 'Ksante',
    'Kennen', 'Naafiri', 'Olaf', 'Gnar', 'Illaoi', 'Irelia', 'Jax', 'Jayce',
    'Kayle', 'Kled', 'Malphite', 'Maokai', 'Mordekaiser', 'Nasus', 'Ornn',
    'Pantheon', 'Poppy', 'Quinn', 'Renekton', 'Riven', 'Sett', 'Shen',
    'Singed', 'Sion', 'Rumble', 'Teemo', 'Urgot', 'Yorick', 'Yone', 'Volibear',
    "Tryndamere"
]

jungle_champions = [
    'Amumu', 'Bel Veth', 'Briar', 'Diana', 'Ekko', 'Elise', 'Evelynn',
    'Fiddlesticks', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Ivern',
    'Jarvan IV', 'Karthus', 'Kayn', 'Kindred', 'Kha\'Zix', 'Lee Sin', 'Lillia',
    'Maokai', 'Naafiri', 'Master Yi', 'Nidalee', 'Nocturne', 'Nunu', 'Poppy',
    'Rengar', 'Rammus', 'Rek\'Sai', 'Sejuani', 'Shaco', 'Skarner', 'Shyvana',
    'Sylas', 'Taliyah', 'Trundle', 'Udyr', 'Vi', 'Viego', 'Volibear',
    'Warwick', 'Xin Zhao', 'Zac', 'Wukong'
]

mid_lane_champions = [
    'Ahri', 'Akali', 'Annie', 'Aurelion Sol', 'Azir', 'Belveth', 'Cassiopeia',
    'Ekko', 'Fizz', 'Galio', 'Kassadin', 'Katarina', 'Kayle', 'LeBlanc',
    'Lissandra', 'Malzahar', 'Orianna', 'Qiyana', 'Ryze', 'Seraphine', 'Sylas',
    'Syndra', 'Talon', 'Twisted Fate', 'Veigar', 'Vex', 'Viktor', 'Vladimir',
    'Xerath', 'Yasuo', 'Yone', 'Zed', 'Ziggs', 'Zilean', 'Zoe', 'Zyra',
    'Anivia', 'Akshan', 'Corki', 'Gragas', 'Irelia', 'Jayce', 'Lux', 'Naafiri',
    'Neeko', 'Pantheon', 'Rumble', 'Swain', 'Tristana', 'Taliyah'
]

adc_champions = [
    'Aphelios', 'Ashe', 'Caitlyn', 'Draven', 'Ezreal', 'Jhin', 'Jinx',
    'Kai\'Sa', 'Kalista', 'Kog\'Maw', 'Miss Fortune', 'Sivir', 'Tristana',
    'Twitch', 'Varus', 'Vayne', 'Xayah', 'Lucian', 'Nilah', 'Samira', 'Yasuo',
    'Zeri'
]

support_champions = [
    'Alistar', 'Bardo', 'Blitzcrank', 'Brand', 'Braum', 'Janna', 'Karma',
    'Leona', 'Lulu', 'Lux', 'Morgana', 'Nami', 'Nautilus', 'Pyke', 'Rakan',
    'Senna', 'Seraphine', 'Sona', 'Soraka', 'Swain', 'Tahm Kench', 'Taric',
    'Thresh', 'Yuumi', 'Zyra', 'Amumu', 'Heimer', 'Maokai', 'Millio',
    'Pantheon', 'Rell', 'Renata', 'Vel Koz', 'Xerath'
]


@client.event
async def on_ready():
  print(f'{client.user} is now running!')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  username = str(message.author)
  user_message = str(message.content)
  channel = str(message.channel)

  print(f'{username} said: "{user_message}" ({channel})')

  if user_message.lower() == '!top':
    response = random.choice(top_lane_champions)
    await message.channel.send(response)

  if user_message.lower() == '!jg':
    response = random.choice(jungle_champions)
    await message.channel.send(response)

  if user_message.lower() == '!mid':
    response = random.choice(mid_lane_champions)
    await message.channel.send(response)

  if user_message.lower() == '!adc':
    response = random.choice(adc_champions)
    await message.channel.send(response)

  if user_message.lower() == '!sup':
    response = random.choice(support_champions)
    await message.channel.send(response)

  if user_message.lower() == '!perso':
    channel_id = message.author.voice.channel.id if message.author.voice else None

    if channel_id:
      if channel_id not in voice_states:
        await message.channel.send("Nenhum membro na call para sortear.")
      else:
        voice_channel_members = voice_states[channel_id]
        if len(voice_channel_members) < 5:
          await message.channel.send(
              "Pelo menos 5 pessoas são necessárias para o sorteio.")
        else:
          random.shuffle(voice_channel_members)
          team1 = voice_channel_members[:5]
          team2 = voice_channel_members[5:]

          team1_names = ', '.join([member.display_name for member in team1])
          team2_names = ', '.join([member.display_name for member in team2])

          await message.channel.send(f'Time Com Camisa: {team1_names}')
          await message.channel.send(f'Time Sem Camisa: {team2_names}')
    else:
      await message.channel.send(
          "Você não está em um canal de voz para usar o comando !perso.")

  else:
    pass


@client.event
async def on_voice_state_update(member, before, after):
  if before.channel != after.channel:
    if before.channel:
      channel_id = before.channel.id
      if channel_id in voice_states and member in voice_states[channel_id]:
        voice_states[channel_id].remove(member)
    if after.channel:
      channel_id = after.channel.id
      if channel_id not in voice_states:
        voice_states[channel_id] = []
      voice_states[channel_id].append(member)


client.run(TOKEN)
