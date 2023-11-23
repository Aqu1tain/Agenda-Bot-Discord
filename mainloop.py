from loader import *
from datetime import date, datetime, timedelta
from icalendar import Calendar
from discord.ext import commands
from translater import *

import keepalive
import discord
import os

TOKEN, CHANNEL_ID = data_tuple(load_config())
CALENDAR_PATH = os.path.abspath("AgendaBotV2/config/calendar.ics")


def setup_bot():
    """
    A function that sets up a bot for Discord communication.

    Returns:
        bot (Bot): The initialized bot object.
    """
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='$', intents=intents)
    bot.remove_command('help')

    @bot.command()
    async def test(ctx, arg):
        """
        A command function that takes a context object and an argument and sends a 
        message to the context with a greeting that includes the argument.

        Parameters:
        ctx (Context): The context object representing the current state of the bot.
        arg (str): The argument to be included in the greeting message.

        Returns:
        None
        """
        await ctx.send(f'Hello {arg}')

    @bot.command(aliases=['cours', 'crs'])
    async def course(ctx, arg="today"):
        """
        Retrieves information about a course.

        Args:
            ctx: The context object.
            arg: The argument that specifies the date of the course. Defaults to "today".

        Returns:
            None
        """
        if arg.lower() == translate(LANGUAGE, 'arguments','today') or arg.lower() == "-n":
            command_date = date.today()
        elif arg.lower() == translate(LANGUAGE, 'arguments','tomorrow') or arg.lower() == "-t":
            command_date = date.today() + timedelta(days=1)
        elif arg.lower() == translate(LANGUAGE, 'arguments','yesterday') or arg.lower() == "-y":
            command_date = date.today() - timedelta(days=1)
        else :
            try :
                command_date = datetime.strptime(arg, "%d/%m/%Y").date()
            except ValueError:
                embedVar = discord.Embed(
                title=translate(LANGUAGE, 'titles', 'Incorrect date format'),
                description=translate(LANGUAGE, 'error', '"The date format is incorrect. Please use the format DD/MM/YYYY. For other arguments, please refer to the help command."'), color=0x3853B4)
                await ctx.send(embed=embedVar)

        with open(CALENDAR_PATH, 'r') as calendar_file:
            ics = Calendar.from_ical(calendar_file.read())
            for event in ics.walk('VEVENT'):
                if event['dtstart'].dt.date() == command_date:
                    embedVar = discord.Embed(
                        title=f":book: {event['summary']} :book:",  # Emoji added here
                        description=str(
                            f":round_pushpin: {translate(LANGUAGE, 'titles', 'Room')}: **{event['location']}**\n"
                            f":man_teacher: {translate(LANGUAGE, 'titles', 'Teacher')}: **{event['prof']}**\n"
                            f":alarm_clock: {translate(LANGUAGE, 'titles', 'Hours')}: **{event['dtstart'].dt.strftime('%H:%M')} - {event['dtend'].dt.strftime('%H:%M')}**"
                        ).replace("Fr�d�ric", "Frédéric").replace("J�r�me", "Jérôme"),
                        color=0x3853B4
                    )
                    await ctx.send(embed=embedVar)
    @bot.command(aliases=['slg'])
    async def set_language(ctx, arg="english"):
        """
        Sets the language for the bot.

        Parameters:
            - ctx (discord.ext.commands.Context): The context of the command.
            - arg (str, optional): The language to set. Defaults to "english".

        Returns:
            None
        
        Raises:
            None
        """
        user = ctx.message.author
        role = discord.utils.find(lambda r: r.id == MODERATOR_ROLE, ctx.message.guild.roles)
        if role in user.roles:
            if arg == "fr": 
                arg = "french"
            elif arg == "en": 
                arg = "english"
            if arg in LANGUAGES_LIST:
                global LANGUAGE
                LANGUAGE = arg
                change_language(arg)
                embedVar = discord.Embed(
                title=f":globe_with_meridians: {translate(LANGUAGE, 'titles', 'Language set')} :globe_with_meridians:",  # Emoji added here
                    description=translate(LANGUAGE, 'descriptions', "Language set to")
                    + f" {translate(LANGUAGE, 'languages', LANGUAGE)}",
                )
                await ctx.send(embed=embedVar)
            else:
                embedVar = discord.Embed(
                    title=translate(LANGUAGE, 'titles', "Incorrect language"),
                    description= translate(LANGUAGE, 'errors', f"That language is not supported. Supported languages are") + f" {LANGUAGES_LIST}",
                )
                await ctx.send(embed=embedVar)
        else:
            embedVar = discord.Embed(
                title=translate(LANGUAGE, 'titles', "Permissions required"),
                description= translate(LANGUAGE, 'errors', f"You need to be a moderator to use this command."),
            )
            await ctx.send(embed=embedVar)
        
    
    @bot.command(aliases=['smdrl'])
    @commands.has_permissions(administrator=True)
    async def setmodrole(ctx, role: discord.Role):
        """
        Sets the moderator role for the bot.

        Parameters:
        - ctx (discord.ext.commands.Context): The context of the command.
        - role (discord.Role): The role to be set as the moderator role.

        Returns: None
        """
        global MODERATOR_ROLE
        MODERATOR_ROLE = role.id
        change_moderator_role(role.id)
        embedVar = discord.Embed(
            title=f":shield: {translate(LANGUAGE, 'titles', 'Moderator role set')} :shield:",  # Emoji added here
            description=translate(LANGUAGE, 'descriptions',
                                  "Moderator role set to") + f" {role.name}",
        )
        await ctx.send(embed=embedVar)

    @bot.command(aliases=['h'])
    async def help(ctx):
        """
        Sends a help message in the form of an embedded message.

        Parameters:
            ctx (discord.Context): The context of the command invocation.

        Returns:
            None
        """
        embedVar = discord.Embed(
            title=f":information_source: {translate(LANGUAGE, 'titles', 'Help')} :information_source:",  # Emoji added here
            description=translate(LANGUAGE, 'descriptions', "The commands are :"),
        )
        for command in bot.commands:
            embedVar.add_field(name=f":wrench: {command.name}", value=command.help, inline=False)  # Emoji added here
        embedVar.set_footer(text=translate(
            LANGUAGE, 'descriptions',
            "For other arguments, please refer to the help command."))
        await ctx.send(embed=embedVar)
   
    @bot.command(aliases=['w', 'weekly', 'semaine'])
    async def week(ctx, num_weeks: int = 0):
        """
        A function that represents a weekly command for the bot.
    
        Parameters:
            ctx (Context): The context of the command.
            num_weeks (int): The number of weeks in the future. Default is 0.
    
        Returns:
            None
        """
        with open(CALENDAR_PATH, 'r') as calendar_file:
            ics = Calendar.from_ical(calendar_file.read())
            embedVar = discord.Embed(
                title=f":calendar: {translate(LANGUAGE, 'titles', 'Weekly schedule')} :calendar:",
                description=translate(LANGUAGE, 'descriptions', "Here is the weekly schedule :"),
                color=0x3853B4
            )
            today = datetime.today().date()
            monday = today - timedelta(days=today.weekday()) + timedelta(weeks=num_weeks)
            sunday = monday + timedelta(days=6)
            days_of_week = [
                translate(LANGUAGE, 'days_of_week', 'Monday'),
                translate(LANGUAGE, 'days_of_week', 'Tuesday'),
                translate(LANGUAGE, 'days_of_week', 'Wednesday'),
                translate(LANGUAGE, 'days_of_week', 'Thursday'),
                translate(LANGUAGE, 'days_of_week', 'Friday'),
                translate(LANGUAGE, 'days_of_week', 'Saturday'),
                translate(LANGUAGE, 'days_of_week', 'Sunday')
            ]
            has_events = False
    
            for day in range(7):
                day_schedule = ""
                day_date = monday + timedelta(days=day)
                for event in ics.walk('VEVENT'):
                    if event['dtstart'].dt.date() == day_date:
                        day_schedule += f"**{event['summary']}** - {event['dtstart'].dt.strftime('%H:%M')}\n"
                        has_events = True
                if day_schedule == "":
                    day_schedule = translate(LANGUAGE, 'titles', 'No events scheduled for this day.')
                embedVar.add_field(name=days_of_week[day], value=day_schedule, inline=False)
    
            if not has_events:
                if today.weekday() == 6:
                    embedVar.add_field(name=translate(LANGUAGE, 'titles', 'Weekly Schedule'), value=translate(LANGUAGE, 'descriptions', 'No more courses for this week.'), inline=False)
                else:
                    embedVar.add_field(name=translate(LANGUAGE, 'titles', 'Weekly Schedule'), value=translate(LANGUAGE, 'descriptions', 'No events scheduled for this week.'), inline=False)
    
            await ctx.send(embed=embedVar)
            
    return bot

def mainloop():
    """
    The main loop of the program.
    """
    global LANGUAGE
    LANGUAGE = get_language()
    global MODERATOR_ROLE 
    MODERATOR_ROLE = get_moderator_role()
    bot = setup_bot()

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')

    keepalive.keep_alive()
    bot.run(TOKEN)


if __name__ == "__main__":
    mainloop()
