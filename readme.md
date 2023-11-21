# Readme.md

## Description

Here is the README.md file. I will provide a short description of the bot. This bot is a simple agenda bot.

## Functionalities

- Add an event
- Remove an event
- Edit an event
- List all events
- List all events from today
- List all events from tomorrow
- List all events from the next 7 days
- List all events from the next 30 days

## Installation

```sh
pip install python3
pip install json
pip install discord.py
```

## Usage

```sh
python3 mainloop.py
```

## Setting up

You need to install this bot on a server that runs the mainloop.py script.
How to correctly setup your server:

- Install python
- Install pip
- Install discord

Create a developer account on the [discord developer portal](https://discord.com/developers/applications).

Create a new application with the following settings:
- Name: Agenda bot, or whatever
- Type: Bot
- Description: Agenda bot, you must credit me '@aquitain'

Give this bot the following permissions:
- Read messages
- Send messages
- Embed links
- Attach files

Copy your TOKEN and paste it in the 'config.json' file.

Go to discord and create a new channel.

Get the ID of your channel and paste it in the 'config.json' file. This will be your main bot channel.

Add your .ics file into the config directory. Rename it 'calendar.ics'.

Run the bot.

## Commentary

This bot has been developed with love by Corentin Renard. 
I made it for my school, to get everyday the courses, and to keep track of them. Hope you enjoy it ❤.

## License

CC-BY-NC-SA 4.0