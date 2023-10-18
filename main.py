import discord
from discord.ext import commands
from datetime import datetime, date, timedelta
from icalendar import Calendar
from config import TOKEN, CHANNEL_ID
from keep_alive import keep_alive
import csv

keep_alive(
)  # Fonction qui appelle UptimeRobot, pour forcer le Bot à être online h24

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='$', intents=intents, help_command=None)


@client.event
async def on_ready():
  print(f'We have logged in as {client.user}'
        )  # Afficher quand le bot est prêt à être utilisé


@client.event
async def on_message(message):
  if message.author == client.user:
    return  # Éviter que le bot se réponde à lui-même

  await client.process_commands(message)


@client.command(name="date", description="Vous renvoie la date")
async def datecommand(ctx):
  todaydate = date.today()
  d1 = todaydate.strftime("%d/%m/%Y")
  await ctx.send('Nous sommes le ' + str(d1))


@client.command(
    name="medias",
    description="Vous renvoie tous les médias conseillés pendant l\'année")
async def mediacommand(ctx):
  embedVar = discord.Embed(
      title="Medias conseillés",
      description="Vous renvoie tous les médias conseillés pendant l\'année",
      color=0x3853B4)
  with open('CSV_Files/medias.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
      for film in row:
        embedVar.add_field(name='',
                           value='**' + str(film) + '**',
                           inline=False)

  await ctx.send(embed=embedVar)


@client.command(
    name="addmedia",
    description="Vous renvoie tous les médias conseillés pendant l\'année")
async def addmediacommand(ctx, nom='NO MEDIA'):
  embedVar = discord.Embed(title="Ajouter un media",
                           description="Vous Avez ajouté le media :" + nom,
                           color=0x3853B4)
  if nom != 'NO MEDIA':
    with open('CSV_Files/medias.csv', a, newline='') as csvfile:
      writer = csv.writer(csvfile, delimiter=',')
      writer.writerow([str(nom)])
    ctx.send(embedVar)
  else:
    return


@client.command(name="cours",
                description="Affiche les cours pour aujourd'hui ou demain")
async def cours_command(ctx, jour="today"):
  # Variables
  courses = []
  horaires = []
  locations = []

  e = open('Agenda/groupeD.ics', 'rb')
  ecal = Calendar.from_ical(e.read())  # Récupérer le calendrier

  # Si l'utilisateur demande les cours pour "aujourd'hui"
  if jour.lower() == "today":
    target_date = date.today()
  # Si l'utilisateur demande les cours pour "demain"
  elif jour.lower() == "demain":
    target_date = date.today() + timedelta(days=1)
  # Si l'utilisateur fournit une date au format jj/mm/aaaa
  else:
    try:
      target_date = datetime.strptime(jour, "%d/%m/%Y").date()
    except ValueError:
      embedVar = discord.Embed(
          title="Erreur de format",
          description=
          "Format de date invalide. Utilisez '**today**', '**demain**' ou une date au format '**jj/mm/aaaa**'.",
          color=0x3853B4)
      await ctx.send(embed=embedVar)

  for event in ecal.walk('VEVENT'):
    Aevent = event.get("DTSTART")
    step = Aevent.dt.date()
    horaire = Aevent.dt.strftime("%Hh%M")
    location = event.get("LOCATION")

    if step == target_date:
      courses.append(event.get("SUMMARY"))
      horaires.append(horaire)
      locations.append(location)

  e.close()

  if len(courses) == 0:
    embedVar = discord.Embed(
        title="Aucun cours",
        description=
        f"Aucun cours prévu pour le {target_date.strftime('%d/%m/%Y')}.",
        color=0x3853B4)
    await ctx.send(embed=embedVar)
  else:
    embedVar = discord.Embed(
        title=f"Emploi du temps {target_date.strftime('%d/%m/%Y')}",
        description=f"Le {target_date.strftime('%d/%m/%Y')}, vous avez : ",
        color=0x3853B4)
    for i in range(min(len(courses), 2)):
      embedVar.add_field(name=courses[i],
                         value=f"{horaires[i]} en **{locations[i].lower()}**",
                         inline=False)
    await ctx.send(embed=embedVar)


@client.command(name="help", description="Affiche les commandes disponibles")
async def help_command(ctx):
  embedVar = discord.Embed(title="Aide pour les commandes",
                           description="Commandes",
                           color=0x3853B4)
  embedVar.add_field(name="$help",
                     value="Demander de l'aide pour les commandes",
                     inline=False)
  embedVar.add_field(name='$date',
                     value='Demander la date du jour',
                     inline=False)
  embedVar.add_field(
      name='$cours [jour]',
      value=
      'Afficher les cours pour aujourd\'hui, demain ou une date spécifique',
      inline=False)
  embedVar.add_field(name='$medias',
                     value='Obtenir les médias conseillés existants',
                     inline=False)
  embedVar.add_field(name='$addmedia',
                     value='Ajouter un média conseillé',
                     inline=False)
  await ctx.send(embed=embedVar)


@client.command(name="ping",
                description="Obtenir ou perdre le rôle Notifs Agenda")
async def ping_command(ctx):
  role_id = 1156174631959531600  # Convertir en int si ce n'est pas déjà le cas
  member = ctx.author
  role = discord.utils.get(ctx.guild.roles, id=role_id)

  if role:
    if role in member.roles:
      await member.remove_roles(role)
      embedVar = discord.Embed(
          title="Rôle",
          description="Le rôle **Notifs Agenda** a bien été enlevé.",
          color=0x3853B4)
      await ctx.send(embed=embedVar)
    else:
      await member.add_roles(role)
      embedVar = discord.Embed(
          title="Rôle",
          description="Le rôle **Notifs Agenda** a bien été ajouté.",
          color=0x3853B4)
      await ctx.send(embed=embedVar)
  else:
    await ctx.send("Le rôle avec l'ID spécifié n'a pas été trouvé.")


# Easter egg, si vous êtes arrivés ici, félicitations à vous
@client.event
async def on_message(message):
  await client.process_commands(message)
  if message.content.startswith('42'):
    embedVar = discord.Embed(
        title="42",
        description=
        "La solution à la grande question sur la vie, l'univers, et le reste, assurément...",
        color=0x3853B4)
    await message.channel.send(embed=embedVar)


client.run(TOKEN)
